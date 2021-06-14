<?php

include __DIR__ . "/worker.php";

class WorkerDB
{
    protected $servername = "localhost";
    protected $username = "local";
    protected $password = "123456";
    protected $dbname = "worker_system";

    public function __destruct()
    {
        // $this->conn->close();
    }
    public function __construct()
    {
        // Create connection
        $conn = new mysqli($this->servername, $this->username, $this->password, $this->dbname);

        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        $conn->close();
        // echo "Connected successfully";
    }

    public function get_all()
    {
        $list_worker = array();

        $conn = new mysqli($this->servername, $this->username, $this->password, $this->dbname);
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        $sql = "SELECT * FROM workers";
        $result = $conn->query($sql);
        if ($result)
            while ($row = $result->fetch_assoc()) {
                $worker = Worker::newByJson(json_encode($row));
                // echo json_encode($row);
                array_push($list_worker, $worker);
            }
        else
            echo "no data";


        return $list_worker;
    }

    function save_change($id, $name, $password, $ip, $queue)
    {
        $conn = new mysqli($this->servername, $this->username, $this->password, $this->dbname);

        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        
        $sql = "UPDATE workers SET name='$name', password='$password', ip='$ip', queue='$queue' WHERE id='$id'";
        $result = $conn->query($sql);

        $conn->close();

        return $result;
    }

    function insert_one($name, $password, $ip, $queue)
    {
        $conn = new mysqli($this->servername, $this->username, $this->password, $this->dbname);
        $id = (new DateTime())->getTimestamp();
        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        $sql = "INSERT INTO  workers (`id`, `name`, `password`, `ip`, `queue`) VALUE ('$id', '$name', '$password', '$ip', '$queue') ";
        // echo $sql;
        $result = $conn->query($sql);

        $conn->close();
        // echo $result.">";
        return $result;
    }
    // public $file_name;

    // function __construct()
    // {
    //     $this -> file_name = __DIR__ . "/localdb/workers.json";
    // }

    // function get_all() {
    //     $myfile = fopen($this->file_name, "r") or die("Unable to open file!");
    //     $file_size = filesize($this->file_name);
    //     $list_worker = array();
    //     if ($file_size> 0)
    //     {
    //         $data = json_decode(fread($myfile, $file_size), true);
    //         foreach ($data as $worker_info) {
    //             $info = json_encode($worker_info);                
    //             $worker = Worker::newByJson($info);
    //             array_push($list_worker, $worker);
    //         } 
    //     }
    //     fclose($myfile);
    //     return $list_worker;
    // }

    // function save_change($worker) {
    //     $list = $this->get_all();
    //     foreach($list as $w) {
    //         if ($w->getId() == $worker->getId())
    //         {
    //             $w->changeInfo( $worker->getName(),  $worker->getPassword(),  $worker->getIP());
    //             break;
    //         }

    //         file_put_contents($this->file_name, json_encode($list));
    //     }
    // }

    // function insert_one($worker) {
    //     $list = $this->get_all();
    //     // array_push($list, $worker);
    //     foreach ($list as $i)
    //         echo json_encode($i);
    //     file_put_contents($this->file_name, json_encode($list));

    // }
}
