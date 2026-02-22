import json
import os
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])
ALLOWED_ORIGIN = os.environ.get('ALLOWED_ORIGIN', '*')


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return int(o) if o % 1 == 0 else float(o)
        return super().default(o)


def cors_headers():
    return {
        'Access-Control-Allow-Origin': ALLOWED_ORIGIN,
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'GET,PUT,DELETE,OPTIONS',
        'Content-Type': 'application/json',
    }


def respond(status, body):
    return {
        'statusCode': status,
        'headers': cors_headers(),
        'body': json.dumps(body, cls=DecimalEncoder),
    }


def get_all_pages():
    result = table.scan(
        ProjectionExpression='slug, title, subtitle, tags, sort_order'
    )
    items = sorted(result.get('Items', []), key=lambda x: x.get('sort_order', 99))
    return respond(200, items)


def get_page(slug):
    result = table.get_item(Key={'slug': slug})
    item = result.get('Item')
    if not item:
        return respond(404, {'error': 'Page not found'})
    return respond(200, item)


def put_page(slug, body):
    item = json.loads(body)
    item['slug'] = slug
    table.put_item(Item=item)
    return respond(200, {'message': f'Page "{slug}" saved', 'slug': slug})


def delete_page(slug):
    table.delete_item(Key={'slug': slug})
    return respond(200, {'message': f'Page "{slug}" deleted'})


def lambda_handler(event, context):
    method = event.get('requestContext', {}).get('http', {}).get('method', '')
    path = event.get('rawPath', '')
    slug = event.get('pathParameters', {})

    if slug:
        slug = slug.get('slug', '')

    try:
        if path == '/api/pages' and method == 'GET':
            return get_all_pages()
        elif path.startswith('/api/pages/') and method == 'GET':
            return get_page(slug)
        elif path.startswith('/api/pages/') and method == 'PUT':
            return put_page(slug, event.get('body', '{}'))
        elif path.startswith('/api/pages/') and method == 'DELETE':
            return delete_page(slug)
        else:
            return respond(404, {'error': 'Not found'})
    except Exception as e:
        print(f'Error: {e}')
        return respond(500, {'error': 'Internal server error'})
