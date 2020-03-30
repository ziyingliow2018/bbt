<!DOCTYPE html>
<html lang="en">
 <!-- Latest compiled and minified CSS -->
 <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css"
 integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">

<head>
    <meta charset="utf-8">
    <meta content="width=device-width, initial-scale=1.0" name="viewport">
    
    <title>SMÖÖ CHÁ</title>

    <link href="assets/vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">
    <!-- <link href="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
    <script src="//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
    <script src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script> -->
    
    <script src="https://code.jquery.com/jquery-2.1.0.min.js" ></script>

    <!--  Main CSS File -->
    <link href="assets/css/logincss.css" rel="stylesheet">
</head>

<body>
    <!-- <div style="background-image:url('/assets/img/background.jpg');"> -->
    <form action="./index.html" method="post">
        <div id="formWrapper">
            <div id="form">
                <div class="logo">
                    <h1 class="text-center head">SMÖÖ CHÁ</h1>
                </div>

                <div class="form-item">
                    <p class="formLabel">Email</p>
                    <input type="email" name="email" id="email" class="form-style" autocomplete="off"/>
                </div>

                <div class="form-item">
                    <p class="formLabel">Password</p>
                    <input type="password" name="password" id="password" class="form-style" />
                    <br>
                    <input type="submit" class="login" value="Sign In"><br><br><hr>
                </div>

                <div class="form-item">
                <?php
                    require ("assets/vendor/vendor/autoload.php");
                    session_start();

                    if(isset($_GET['state'])) {
                        $_SESSION['FBRLH_state'] = $_GET['state'];
                    }

                    /*Step 1: Enter Credentials*/
                    $fb = new \Facebook\Facebook([
                        'app_id' => '134169310679094',
                        'app_secret' => '264b5647eabf27806a5122d127df8dc7',
                        'default_graph_version' => 'v2.12',
                        //'default_access_token' => '{access-token}', // optional
                    ]);


                    /*Step 2 Create the url*/
                    if(empty($access_token)) {

                        echo "<a href='{$fb->getRedirectLoginHelper()->getLoginUrl("http://localhost/bbt/index.html")}'>Login with Facebook </a>";
                    }

                    /*Step 3 : Get Access Token*/
                    $access_token = $fb->getRedirectLoginHelper()->getAccessToken();


                    /*Step 4: Get the graph user*/
                    if(isset($access_token)) {


                        try {
                            $response = $fb->get('/me',$access_token);

                            $fb_user = $response->getGraphUser();

                            echo  $fb_user->getName();




                            //  var_dump($fb_user);
                        } catch (\Facebook\Exceptions\FacebookResponseException $e) {
                            echo  'Graph returned an error: ' . $e->getMessage();
                        } catch (\Facebook\Exceptions\FacebookSDKException $e) {
                            // When validation fails or other local issues
                            echo 'Facebook SDK returned an error: ' . $e->getMessage();
                        }

                    }
                    ?>
                </div>
            </div>
        </div>
    </form>
<!-- </div> -->
</body>
</html>