<?php


namespace App\Repositories;


use App\Models\User;

class UserRepository
{
    function startConditions()
    {
        return app(User::class);
    }
    public function getAllWithPaginateAndFiltering()
    {
        $perPage = request('perPage');
        $columns = [
            'id',
            'name',
            'email',
            'role',
            'created_at as reg_time',
            'notifications_receiver',
        ];

        return $this->startConditions()
            ->select($columns)
            ->filter()
            ->paginate($perPage);
    }
    public function changeRole($id, $newRole) {
        $this->startConditions()
            ->where('id',$id)
            ->update(['role'=>$newRole]);
    }
    public function changeNewsReceivers($id, $newState) {
        $this->startConditions()
            ->where('id',$id)
            ->update(['notifications_receiver'=>$newState]);
    }
}
