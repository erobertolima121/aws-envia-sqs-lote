import boto3
import time

# Configurações
queue_url = 'sua-fila'
aws_access_key_id = 'aws_access_key_id'
aws_secret_access_key = 'aws_secret_access_key'
region_name = 'sa-east-1'

# Inicializa o cliente SQS
sqs = boto3.client(
    'sqs',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

# Gera 10 mensagens
messages = [
    {'Id': f'msg{i}', 'MessageBody': f'Mensagem {i}'}
    for i in range(1, 10)
]


# Função para dividir em lotes de até 10
def chunked(iterable, n):
    for i in range(0, len(iterable), n):
        yield iterable[i:i + n]


# Medir TPS
total_sent = 0
start_time = time.time()

for batch in chunked(messages, 10):
    response = sqs.send_message_batch(
        QueueUrl=queue_url,
        Entries=batch
    )
    total_sent += len(batch)

end_time = time.time()
elapsed = end_time - start_time
tps = total_sent / elapsed if elapsed > 0 else 0

print(f'Total de mensagens enviadas: {total_sent}')
print(f'Tempo total: {elapsed:.2f} segundos')
print(f'Throughput (TPS): {tps:.2f} mensagens/segundo')
