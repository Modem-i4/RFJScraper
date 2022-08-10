<?php

namespace App\Http\Controllers;


use App\Models\Notification;
use App\Repositories\NotificationRepository;
use App\Repositories\ProfileRepository;

class NotificationController extends Controller
{
    private $repos;
    public function __construct()
    {
        $this->middleware('auth');

        $this->repos = app(NotificationRepository::class);
    }
    public function changeSubscribe($id, $checked)
    {
        return $this->repos->changeSubscribe($id, $checked == 'true');
    }
}
