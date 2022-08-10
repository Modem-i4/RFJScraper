<?php


namespace App\Repositories;


use App\Models\Post;

class PostRepository
{
    function startConditions()
    {
        return app(Post::class);
    }
    public function getAllWithPaginateAndFiltering()
    {
        $perPage = request('perPage');
        $columns = [
            'base.id',
            'base.text',
            'base.images',
            'base.url',
            'base.published_at',
            'base.important',
            'base.categories',
            'base.status',

            'profiles.id as profile_id',
            'profiles.name',
            'profiles.url as profile_url',
            'profiles.is_group',
        ];
        return $this->startConditions()
            ->from('posts as base')
            ->select($columns)
            ->join('profiles', 'base.poster_id', '=', 'profiles.id')
            ->filter()
            ->where('base.removed', 0)
            ->paginate($perPage);
    }
    public function changeImportance($id, $importance) {
        $this->startConditions()
            ->where('id', $id)
            ->update(['important' => $importance]);
    }
    public function changeCategories($id) {
        $categories = request('categories');
        $this->startConditions()
            ->where('id', $id)
            ->update(['categories' => $categories]);
    }
    public function remove($id) {
        $this->startConditions()
            ->where('id', $id)
            ->update([
                    'removed' => 1,
                    'html' => '',
                ]);
    }
    public function getTwitterScreenshotIfExist($id) {
        return $this->startConditions()
            ->select('html')
            ->where('id', $id)
            ->where('url', 'LIKE', '%twitter.com/%')
            ->first();
    }
}
