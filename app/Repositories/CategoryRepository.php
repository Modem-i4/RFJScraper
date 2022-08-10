<?php


namespace App\Repositories;


use App\Models\Category;
use Illuminate\Support\Facades\DB;

class CategoryRepository
{
    function startConditions()
    {
        return app(Category::class);
    }
    public function getAll()
    {
        $perPage = request('perPage');
        $columns = [
            'base.id',
            'base.name',
            'base.display',
            DB::raw('COUNT(posts.id) as total'),
        ];
        return $this->startConditions()
            ->from('categories as base')
            ->select($columns)
            ->leftJoin('posts', function($join) {
                $join->on('posts.categories', 'LIKE', DB::raw('CONCAT("%,", base.id ,",%")'))
                    ->orOn('posts.categories', 'LIKE', DB::raw('CONCAT("[", base.id ,",%")'))
                    ->orOn('posts.categories', 'LIKE', DB::raw('CONCAT("%,", base.id ,"]")'))
                    ->orOn('posts.categories', 'LIKE', DB::raw('CONCAT("[", base.id ,"]")'));
            })
            ->groupBy('id')
            ->filter()
            ->where('base.removed', 0)
            ->paginate($perPage);
    }
    public function getNames() {
        $columns = [
            'id',
            'name',
            'display',
        ];
        return $this->startConditions()
            ->from('categories')
            ->select($columns)
            ->get();
    }
    public function add()
    {
        $name = request('name');
        $success = $this->startConditions()
            ->select('profiles')
            ->insert([
                'name' => $name,
            ]);
        if ($success) {
            return response(200);
        }
    }
    public function changeDisplay($id, $checked) {
        $this->startConditions()
            ->where('id', $id)
            ->update(['display' => $checked]);
    }
    public function remove($id) {
        $this->startConditions()
            ->where('id', $id)
            ->update([
                'display' => 0,
                'removed' => 1,
                ]);
    }
}
