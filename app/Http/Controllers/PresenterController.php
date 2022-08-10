<?php

namespace App\Http\Controllers;

use App\Repositories\PresenterRepository;
use Illuminate\Http\Request;

class PresenterController extends Controller
{
    private $repos;
    public function __construct()
    {
        $this->middleware('auth');

        $this->repos = app(PresenterRepository::class);
    }
    public function get($id)
    {
        $data = $this->repos->get($id);
        if($data === null)
            return redirect('posts');
        $uid = $data->uid;
        $site = strpos($data->url, "https://www.instagram.com/") !== false ? "Instagram" :
                strpos($data->url, "https://twitter.com/") !== false ? "Twitter" : "Facebook";
        $isInstagramPost = strpos($data->url, "https://www.instagram.com/p/") !== false;
        return view('templates.post', ['uid' => $uid, 'site' => $site, 'isInstagramPost' => $isInstagramPost]);
    }
}
