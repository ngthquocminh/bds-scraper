<?php
    include  dirname(dirname(__FILE__)) . "/utilities/database.php";
    $database = new WorkerDB();
    
    $list_wokers = $database->get_all();
    
    $action = isset($_GET["do"]) ? $_GET["do"] : null;
    $page = isset($_GET["page"]) ? $_GET["page"] : null;
    $algth = isset($_GET["algth"]) ? $_GET["algth"] : null;
    
    $edit = false;
    if (($action == "crawling" || $action == "parsing") && $page != null) {
        $edit = true;
    }

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
        <?php 
            if ($action == "crawling" || $action == "parsing") {
                echo "
                <ul>
                    <li>
                        <a href='?do=$action&page=nhadat247.com.vn' class=\"list-site btn btn-primary\"> 
                            nhadat247.com.vn
                        </a>
                    </li>
                    <li>
                        <a href='?do=$action&page=nha.chotot.com' class=\"list-site btn btn-primary\">
                            nha.chotot.com
                        </a>
                    </li>
                    <li>
                        <a href='?do=$action&page=batdongsan.com.vn' class=\"list-site btn btn-primary\">
                            batdongsan.com.vn
                        </a>
                    </li>
                </ul>";
            }
        ?>
        <hr style="margin: 50px 0">
        <?php
            $form_title = "";
            if ($edit){
                $form_title = "
                    <h4>Config ".($action=="crawling"?"Crawler":"Parser")." for: <b>$page</b></h4>
                ";
            }
            
        ?>

        <form <?php echo  $edit && $action=="parsing" && $algth != null ? "" : "style='display: none'"; ?>; action="">
            <h5><?php echo $form_title ?></h5>
            <h6>Xpath selector</h6>
            <div class="input-group mb-3">
                <div class="input-group-prepend">
                    <span class="input-group-text">Title</span>
                </div>
                <input name="name" type="text" value="//*[@id='product-detail-web']/div[1]/h1/text()" class="form-control" placeholder="Workername" required>
            </div> 
            <div class="input-group mb-3">
                <div class="input-group-prepend">
                    <span class="input-group-text">Category</span>
                </div>
                <input name="name" type="text" value="//*[@id='product-detail-web']/div[6]/div[2]/div/div[1]" class="form-control" placeholder="Workername" required>
            </div> 
            <div class="input-group mb-3">
                <div class="input-group-prepend">
                    <span class="input-group-text">Description</span>
                </div>
                <input name="name" type="text" value="//*[@id='product-detail-web']/div[2]" class="form-control" placeholder="Workername" required>
            </div> 
            <div class="input-group mb-3">
                <div class="input-group-prepend">
                    <span class="input-group-text">Region</span>
                </div>
                <input name="name" type="text" value="/html/body/div[1]/div[7]/div[1]/section/div[1]/div[3]/a[2]/text()" class="form-control" placeholder="Workername" required>
            </div> 
            <div class="input-group mb-3">
                <div class="input-group-prepend">
                    <span class="input-group-text">Street</span>
                </div>
                <input name="name" type="text" value="/html/body/div[5]/div[1]/div/div[1]/div[1]/div[1]/a[1]/text()" class="form-control" placeholder="Workername" required>
            </div>     
            <button type="submit" class="btn btn-primary">Submit</button>       
        </form>

        <form <?php echo  $edit && $action=="parsing" && $algth == null ? "" : "style='display: none'"; ?>; action="">
            <h5><?php echo $form_title ?></h5>
            <h6>Choose Algorithm</h6>

            <a href="<?php echo "?do=".$action."&page=".$page."&algth=xpth"; ?>" class="btn btn-primary">Xpath-regex</a>
            <a href="<?php echo "?do=".$action."&page=".$page."&algth=line"; ?>" class="btn btn-primary">Line-select</a>
            <a href="<?php echo "?do=".$action."&page=".$page."&algth=auto"; ?>" class="btn btn-primary">Auto-parser</a>
        </form>

        <form <?php echo  $edit && $action=="crawling" ? "" : "style='display: none'"; ?>; action="">
            <h5><?php echo $form_title ?></h5>
            <h6>Url regex</h6>
            <div class="input-group mb-3">
                <div class="input-group-prepend">
                    <span class="input-group-text">Sub-url</span>
                </div>
                <input name="name" type="text" value="https[:][/][/]batdongsan[\.]com[\.]vn/ban-[-a-z0-9]+(/p[0-9]+)?" class="form-control" placeholder="Workername" required>
            </div>
            <div class="input-group mb-3">
                <div class="input-group-prepend">
                    <span class="input-group-text">Url post</span>
                </div>
                <input name="name" type="text" value="https[:][/][/]batdongsan[\.]com[\.]vn/ban-[-a-z0-9]+/[-a-z0-9]+pr[0-9]+" class="form-control" placeholder="Workername" required>
            </div>
            <h6>Key type</h6>
            <div class="input-group mb-3">
                <div class="input-group-prepend">
                    <span class="input-group-text">Nhà ở</span>
                </div>
                <input name="name" type="text" value="ban-nha-rieng, ban-nha-biet-thu, ban-nha-mat-pho" class="form-control" placeholder="Workername" required>
            </div>
            <div class="input-group mb-3">
                <div class="input-group-prepend">
                    <span class="input-group-text">Đất</span>
                </div>
                <input name="name" type="text" value="ban-dat" class="form-control" placeholder="Workername" required>
            </div>
            <div class="input-group mb-3">
                <div class="input-group-prepend">
                    <span class="input-group-text">Căn hộ/chung cư</span>
                </div>
                <input name="name" type="text" value="ban-can-ho-chung-cu" class="form-control" placeholder="Workername" required>
            </div>
            
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    </div>
</div>
</body>
<script src="https://kit.fontawesome.com/31cb90300c.js" crossorigin="anonymous"></script>
</html>

<?php



?>