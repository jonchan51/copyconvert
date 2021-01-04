import cloudconvert
import logging
from urllib.request import urlretrieve


def _create_convert_job(output_format):
    return cloudconvert.Job.create(payload={
        "tasks": {
            'upload': {
                'operation': 'import/upload'
            },
            'convert': {
                'operation': 'convert',
                'input': 'upload',
                'output_format': output_format
            },
            'export': {
                'operation': 'export/url',
                'input': 'convert'
            }
        }
    })


def _upload_file(fp, job):
    # what if it fails?
    upload_task_id = job['tasks'][0]['id']
    upload_task = cloudconvert.Task.find(id=upload_task_id)
    return cloudconvert.Task.upload(file_name=fp, task=upload_task)


def _download_file(job):
    download_task_id = job['tasks'][2]['id']
    res = cloudconvert.Task.wait(id=download_task_id)
    f = res.get('result').get('files')[0]
    try:
        url = f['url']
        logging.debug(f'Attempting to download from {url}')
        filename, _ = urlretrieve(url)
        logging.debug(f'Downloaded from {url}')
        return filename
    except Exception as e:
        logging.error(
            f'Encountered exception while downloading from url: {url}')
    return None


def convert(fp, output_format):
    """Converts given file to output_format.
    """
    logging.debug(f'Attempting to convert {fp} to {output_format}')
    job = _create_convert_job(output_format)
    _upload_file(fp, job)
    new_file = _download_file(job)
    logging.debug(f'Converted {fp} to {output_format}')
    return new_file
