<?php

namespace App\Http\Controllers;

use App\Repositories\PostRepository;
use Illuminate\Http\Request;

class PostController extends Controller
{
    private $repos;
    public function __construct()
    {
        $this->middleware('auth');

        $this->repos = app(PostRepository::class);
    }
    public function index() {
        return view('admin.posts');
    }
    public function all()
    {
        return $this->repos->getAllWithPaginateAndFiltering();
    }
    public function changeImportance($id, $importance)
    {
        $result = $this->repos->changeImportance($id, $importance == 'true');
    }
    public function changeCategories($id) {
        $result = $this->repos->changeCategories($id);
    }
    public function remove($id) {
        $screenshotFile = $this->repos->getTwitterScreenshotIfExist($id);
        if($screenshotFile !== null) {
            unlink("screenshots/tweets/$screenshotFile->html.png");
        }
        $result = $this->repos->remove($id);
    }
}
