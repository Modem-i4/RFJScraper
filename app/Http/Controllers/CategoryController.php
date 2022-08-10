<?php

namespace App\Http\Controllers;

use App\Repositories\CategoryRepository;
use Illuminate\Http\Request;

class CategoryController extends Controller
{
    private $repos;
    public function __construct()
    {
        $this->middleware('auth');

        $this->repos = app(CategoryRepository::class);
    }
    public function index() {
        return view('admin.categories');
    }
    public function all()
    {
        return $this->repos->getAll();
    }
    public function getNames()
    {
        return $this->repos->getNames();
    }
    public function add()
    {
        return $this->repos->add();
    }
    public function changeDisplay($id, $checked)
    {
        return $this->repos->changeDisplay($id, $checked == 'true');
    }
    public function remove($id) {
        return $this->repos->remove($id);
    }
}
