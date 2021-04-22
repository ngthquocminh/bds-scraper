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
        <ul class="row ul-none-style"> 
            <li class="col-sm-4">
                <div class="dropdown">
                    <a href="pages/worker_setup.php" class="my-a">
                        Setup Worker
                    </a>
                </div>
            </li>
            <li class="col-sm-4">
                <div class="dropdown">
                    <span>
                        Configuration
                    </span>
                    <div class="dropdown-content">
                        <div> <a href="/pages/configuration.php?do=crawling"> Crawling </a></div>
                        <div><a href="/pages/configuration.php?do=parsing"> Parsing</a></div>

                    </div>
                </div>
            </li>
            <li class="col-sm-4">
                <div class="dropdown">
                    <span>
                        Workers Controller
                    </span>
                    <div class="dropdown-content">
                        <div> <a href="/pages/workerscontroller.php?do=crawling"> Crawling </a></div>
                        <div><a href="/pages/workerscontroller.php?do=parsing"> Parsing</a></div>
                    </div>
                </div>
            </li>
        </ul>
    </div>
</body>
<script src="https://kit.fontawesome.com/31cb90300c.js" crossorigin="anonymous"></script>
</html>

<?php



?>