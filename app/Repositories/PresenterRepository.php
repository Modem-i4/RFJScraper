<?php


namespace App\Repositories;


use App\Models\Post;

class PresenterRepository
{
    function startConditions()
    {
        return app(Post::class);
    }
    public function get($id)
    {
        $columns = [
            'uid',
            'url',
        ];
        return $this->startConditions()
            ->select($columns)
            ->where('id', $id)
            ->first();
    }
}
