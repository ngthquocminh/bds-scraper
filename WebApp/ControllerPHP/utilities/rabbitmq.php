<?php 

    require_once __DIR__ . '/vendor/autoload.php';
    use PhpAmqpLib\Connection\AMQPStreamConnection;
    use PhpAmqpLib\Message\AMQPMessage;

    $connection = new AMQPStreamConnection('20.198.248.42', 5672, 'worker01', 'worker01');
    $channel = $connection->channel();

    $channel->queue_declare('hello1', false, false, false, false);

    $msg = new AMQPMessage('Hello World! PHP');
    $channel->basic_publish($msg, '', 'hello1');

    echo " [x] Sent 'Hello World!'\n";

    $channel->close();
    $connection->close();
    

?>