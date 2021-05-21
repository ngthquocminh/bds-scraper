<?php
    include  dirname(dirname(__FILE__)) . "/utilities/database.php";
    $database = new WorkerDB();
    
    $list_wokers = $database->get_all();
    
    $action = isset($_GET["do"]) ? $_GET["do"] : "";
    // $id = isset($_GET["id"]) ? $_GET["id"] : "";
    // echo $id;

?>

<!DOCTYPE html>
<html lang="vi">

<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="/css/main.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js" integrity="sha384-JEW9xMcG8R+pH31jmWH6WWP0WintQrMb4s7ZOdauHnUtxwoG2vI5DkLtS3qm9Ekf" crossorigin="anonymous"></script>
    <title>Crawlers System</title>

    <style>
        .list-site {
            margin-top: 20px
        }
        </style>
</head>

<body>
<div class="jumbotron text-center" style="margin-top: 50px;">
        <h1>WORKER CONTROLLER SYSTEM</h1>
        <!-- <p>Resize this responsive page to see the effect!</p> -->
    </div>
    <div class="container">
        <div><a href="/">Home</a> / <?php echo ucfirst($action); ?> Configuration</div>
        <?php if ($action == "crawling") echo "<ul>
            <li>
                <button type=\"button\" class=\"list-site btn btn-primary\"> 
                    https://nhadat247.com.vn/ 
                </button>
            </li>
            <li>
                <button type=\"button\" class=\"list-site btn btn-primary\">
                    https://nha.chotot.com/
                </button>
            </li>
        </ul>";
        ?>
    </div>
</div>
</body>
<script src="https://kit.fontawesome.com/31cb90300c.js" crossorigin="anonymous"></script>
</html>

<?php



?>