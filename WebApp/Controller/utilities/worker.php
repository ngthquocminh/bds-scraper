<?php

class Worker {
    
    protected $id;
    protected $name;
    protected $password;
    protected $ip;

    public function __construct($name, $password, $ip)
    {
        $this->name = $name;
        $this->password = $password;
        $this->ip = (string)$ip;
        $this->id = (new DateTime())->getTimestamp();
    }

    public static function newFull($id, $name, $password, $ip)
    {
        $new = new Worker($name, $password, $ip);
        $new->id = $id;
        return $new;
    }


    public function getName() {
        return $this->name;
    }

    public function getIP() {
        return $this->ip;
    }

    public function getPassword() {
        return $this->password;
    }

    public function getId() {
        return $this->id;
    }
    
    public function changeInfo($name, $password, $ip)
    {
        $this->name = $name;
        $this->password = $password;
        $this->ip = (string)$ip;
    }

    public static function newByJson($json) {
        $worker_data = json_decode($json);
        $new_worker = new Worker($worker_data->{"name"}, $worker_data->{"password"}, $worker_data->{"ip"});
        $new_worker->id = $worker_data->{"id"};

        return $new_worker;
    }


}

?>