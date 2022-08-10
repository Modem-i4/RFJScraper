<?php

namespace App\Http\Controllers;

use App\Repositories\SettingRepository;

class SettingController extends Controller
{
    private $repos;
    public function __construct()
    {
        $this->middleware('auth');

        $this->repos = app(SettingRepository::class);
    }
    public function index() {
        return view('admin.settings');
    }
    public function all()
    {
        return $this->repos->getAll();
    }
    public function save($id, $newValue)
    {
        return $this->repos->save($id, $newValue);
    }
}
