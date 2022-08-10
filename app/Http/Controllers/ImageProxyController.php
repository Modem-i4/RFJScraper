<?php
namespace App\Http\Controllers;

class ImageProxyController extends Controller {
    public function get(){
        $url = urldecode($_GET["url"]);
        return base64_encode(file_get_contents($url));
    }
}
