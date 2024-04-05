<?php

$is_invalid = false;

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    
    $mysqli = require __DIR__ . "/database.php";
    
    $sql = sprintf("SELECT * FROM user
                    WHERE email = '%s'",
                   $mysqli->real_escape_string($_POST["email"]));
    
    $result = $mysqli->query($sql);
    
    $user = $result->fetch_assoc();
    
    if ($user) {
        
        if (password_verify($_POST["password"], $user["password_hash"])) {
            
            session_start();
            
            session_regenerate_id();
            
            $_SESSION["user_id"] = $user["id"];
            
            header("Location: index.php");
            exit;
        }
    }
    
    $is_invalid = true;
}

?>
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="loginpage02.css">
</head>
<body>
    
    
    
    <?php if ($is_invalid): ?>
        <em>Invalid login</em>
    <?php endif; ?>
    <div class="content">
        <div class="text">LOGIN</div>
    <form method="post">
            <div class="field">
              <span class="fa fa-user"></span>
              <input type="email" placeholder="USERNAME" id="email"
                     value="<?= htmlspecialchars($_POST["email"] ?? "") ?>">
            </div>
          
            <div class="field">
              <span class="fa fa-lock"></span>
              <input type="password" placeholder="PASSWORD">
            </div>
        </form>
        <br><br>
        <p class="para-2">
            NOT A MEMBER? <a href="loginpage02.html">SIGN UP NOW</a>
        </p>
        <br><br>
        <a href="MAINFRONTPAGELOGINOUT.html">
            <button class="registerbtn" type="sumbit">Log in</button>
        </a>

        
        
    </form>
    
</body>
</html>


<!--
    
    <label for="password">Password</label>
    <input type="password" name="password" id="password">
-->