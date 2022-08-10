<?php


namespace App\Repositories;


use App\Models\Notification;
use Illuminate\Support\Facades\Auth;

class NotificationRepository
{
    function startConditions()
    {
        return app(Notification::class);
    }
    public function changeSubscribe($id, $checked) {
        $user_id = Auth::id();
        if($checked) {
            $this->startConditions()
                ->insert([
                    'profile_id' => $id,
                    'user_id' => $user_id
                ]);
        }
        else {
            $this->startConditions()
                ->where('profile_id', $id)
                ->where('user_id', $user_id)
                ->delete();
        }
    }
}
