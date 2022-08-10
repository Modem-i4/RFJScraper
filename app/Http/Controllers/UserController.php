<?php

namespace App\Http\Controllers;

use App\Repositories\UserRepository;

class UserController extends Controller
{
    private $repos;
    public function __construct()
    {
        $this->middleware('auth');

        $this->repos = app(UserRepository::class);
    }
    public function index() {
        return view('admin.users');
    }
    public function all()
    {
        return $this->repos->getAllWithPaginateAndFiltering();
    }
    public function changeRole($id, $newRole) {
        $response = $this->repos->changeRole($id, $newRole);
    }
    public function changeNewsReceivers($id, $newState) {
        $response = $this->repos->changeNewsReceivers($id, $newState === 'true');
    }
}
