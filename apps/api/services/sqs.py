import boto3
import json
from config import config_settings

def _get_sqs_client():
    """
    Creates an SQS client. In development, it uses the ElasticMQ endpoint. In production, it uses the AWS SQS service.

    """
    kwargs = {
        'region_name': config_settings.aws_region
    }
    if config_settings.sqs_endpoint:
        kwargs['endpoint_url'] = config_settings.sqs_endpoint
    return boto3.client('sqs', **kwargs)

def send_batch_messages(messages: list[dict]) -> None:
    """
    Sends a batch of messages to the SQS queue.

    Args:
        messages (list[dict]): A list of messages to send.
    """
    sqs = _get_sqs_client()

    for i in range(0, len(messages), 10):
        batch = messages[i:i+10]
        entries = [{'Id': str(j), 'MessageBody': json.dumps(msg)} for j, msg in enumerate(batch)]
        try:
            sqs.send_message_batch(QueueUrl=config_settings.sqs_queue, Entries=entries)
        except Exception as e:
            raise RuntimeError(f"Error sending batch messages to SQS: {e}") from e

def receive_messages(maximum: int = 10) -> list[dict]:
    """
    Receives messages from the SQS queue.

    Args:
        maximum (int): The maximum number of messages to receive.
    
    Returns:
        list[dict]: A list of messages received from the queue.
    """
    sqs = _get_sqs_client()
    try:
        response = sqs.receive_message(QueueUrl=config_settings.sqs_queue, MaxNumberOfMessages=maximum)
        messages = response.get('Messages', [])
        return messages
    except Exception as e:
        raise RuntimeError(f"Error receiving messages from SQS: {e}") from e

def delete_messages(receipt_handle: str) -> None:
    """
    Deletes messages from the SQS queue.

    Args:
        receipt_handle (str): The receipt handle of the message to delete.
    """
    sqs = _get_sqs_client()
    try:
        sqs.delete_message(QueueUrl=config_settings.sqs_queue, ReceiptHandle=receipt_handle)
    except Exception as e:
        raise RuntimeError(f"Error deleting message from SQS: {e}") from e
