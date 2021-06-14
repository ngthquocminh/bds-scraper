<?php

include  dirname(dirname(__FILE__)) . "/utilities/database.php";
$database = new WorkerDB();

$list_wokers = $database->get_all();

$edit = isset($_GET["action"]) ? $_GET["action"] : "";
$id = isset($_GET["id"]) ? $_GET["id"] : "";
// echo $id;

$current_worker = null;
foreach ($list_wokers as $worker) {
    if ($worker->getId() == $id) {
        $current_worker  = $worker;
        break;
    }
}
if ($edit == "save") {
    // echo "save";
    $_id = isset($_GET["id"]) ? $_GET["id"] : "";
    $_name = isset($_GET["name"]) ? $_GET["name"] : "";
    $_pass = isset($_GET["password"]) ? $_GET["password"] : "";
    $_queue = isset($_GET["queue"]) ? $_GET["queue"] : "";
    $_ip = isset($_GET["ip"]) ? $_GET["ip"] : "";
    // echo $_id. $_name. $_pass;
    if ($current_worker != null) {
        $current_worker->changeInfo($_name, $_pass, $_ip, $_queue);
        $database->save_change($_id, $_name, $_pass, $_ip, $_queue);
    } else {
        if ($database->insert_one($_name, $_pass, $_ip, $_queue)) {
            $_new = new Worker($_name, $_pass, $_ip, $_queue);
            array_push($list_wokers, $_new);
        }

    }
    header("Location: ".__DIR__."worker_setup.php");
    // echo $actual_link;
}

$form_title = $edit == "edit" ? "Edit Worker ID: " . $id : ($edit == "new" ? "New Worker" : "");
$form_display = ($edit == "edit" && $current_worker != null || $edit == "new") ? true : false

?>

<!DOCTYPE html>
<html lang="vi">

<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="/css/main.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js" integrity="sha384-JEW9xMcG8R+pH31jmWH6WWP0WintQrMb4s7ZOdauHnUtxwoG2vI5DkLtS3qm9Ekf" crossorigin="anonymous"></script>
    <title>Crawlers System</title>
</head>

<body>
    <div class="jumbotron text-center" style="margin-top: 50px;">
        <h1>WORKER CONTROLLER SYSTEM</h1>
        <!-- <p>Resize this responsive page to see the effect!</p> -->
    </div>
    <div class="container">
        <div><a href="/">Home</a> / Worker Setup</div>
        <table id="workers-list" class="table">
            <thead>
                <tr>
                    <th>No.</th>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Pass</th>
                    <th>IP</th>
                    <th>Queue</th>
                    <th>.</th>
                    <th>.</th>
                    <th>.</th>
                </tr>
            </thead>
            <tbody>

                <?php
                $no = 0;
                foreach ($list_wokers as $worker) {
                    $no++;
                    $id = $worker->getId();
                    $name = $worker->getName();
                    $password = $worker->getPassword();
                    $ip = $worker->getIP();
                    $queue = $worker->getQueue();
                    echo
                    "
                        <tr>
                            <td>$no</td>
                            <td>$id</td>
                            <td>$name</td>
                            <td>$password</td>
                            <td>$ip</td>
                            <td>$queue</td>
                            <td><a href=\"?action=edit&id=$id\"><i class=\"far fa-edit\"></a></i></td>
                            <td><a href=\"?action=edit&id=$id\"><i class=\"far fa-trash-alt\"></i></a></i></td>
                            <td><button class=\"round-border\"><i class=\"fas fa-play-circle\"></i> test connection</button></i></td>
                        </tr>
                        ";
                }

                ?>


            </tbody>
        </table>
        <a class="a-button my-a" href="?action=new">Add new worker</a>
        <hr style="margin: 50px 0">

        <form <?php echo  $form_display ? "" : "style=\"display: none\""; ?>; action="/pages/worker_setup.php">
            <h5><?php echo $form_title ?></h5>
            <div class="input-group mb-3">
                <div class="input-group-prepend">
                    <span class="input-group-text">Workername</span>
                </div>
                <input name="name" type="text" value="<?php echo $current_worker != null ? $current_worker->getName() : ''; ?>" class="form-control" placeholder="Workername" required>
            </div>

            <div class="input-group mb-3">
                <div class="input-group-append">
                    <span class="input-group-text">Password</span>
                </div>
                <input name="password" type="text" value="<?php echo $current_worker != null ? $current_worker->getPassword() : ''; ?>" class="form-control" placeholder="RabbitMQ pasword" required>

            </div>
            <div class="input-group mb-3">
                <div class="input-group-append">
                    <span class="input-group-text">Worker's IP</span>
                </div>
                <input name="ip" type="text" value="<?php echo $current_worker != null ? $current_worker->getIP() : ''; ?>" class="form-control" placeholder="Worker IP" required>

            </div>
            <div class="input-group mb-3">
                <div class="input-group-append">
                    <span class="input-group-text">Queue Name</span>
                </div>
                <input name="queue" type="text" value="<?php echo $current_worker != null ? $current_worker->getQueue() : ''; ?>" class="form-control" placeholder="Queue Name" required>

            </div>
            <input name="action" type="text" class="form-control" value="save" style="display: none;" required>
            <input <?php echo $edit == "edit" ? "name='id' value='" . ($current_worker != null ? $current_worker->getId() : "") . "'" : ""; ?> type="text" class="form-control" style="display: none;">

            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    </div>
</body>
<script src="https://kit.fontawesome.com/31cb90300c.js" crossorigin="anonymous"></script>

</html>

<?php



?>