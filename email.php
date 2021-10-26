<?php

$email = $_GET['email'];
$sanitized = filter_var($email, FILTER_SANITIZE_EMAIL);
if (filter_var($sanitized, FILTER_VALIDATE_EMAIL)) {
  echo "Before: $email";
  echo "<hr>";
  echo "After:  $sanitized";    
} else {
  echo "Invalid";
}

?>
