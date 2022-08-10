<?php


namespace App\Repositories;


use App\Models\Profile;
use Illuminate\Support\Facades\DB;

class ProfileRepository
{
    function startConditions()
    {
        return app(Profile::class);
    }
    public function getAllWithPaginateAndFiltering()
    {
        $perPage = request('perPage');
        $columns = [
            'profiles.id',
            'profiles.name',
            'profiles.url',
            'profiles.is_group',
            'profiles.watched',
            DB::raw('MAX(posts.published_at) as last_publish'),
            DB::raw('COUNT(posts.id) as total_posts'),
            DB::raw('SUM(published_at >= CURDATE() - INTERVAL 6 DAY) as last_7_days'),
            DB::raw('SUM(published_at >= CURDATE() - INTERVAL 29 DAY) as last_30_days'),       
            DB::raw('COUNT(notifications.profile_id) as subscribe')
        ];

        return $this->startConditions()
            ->leftJoin('posts','poster_id','=','profiles.id')
            ->leftJoin('notifications','profile_id','=','profiles.id')
            ->select($columns)
            ->groupBy('name')
            ->filter()
            ->where('profiles.removed', 0)
            ->paginate($perPage);
    }
    public function changeWatch($id, $checked) {
        $this->startConditions()
            ->where('id', $id)
            ->update(['watched' => $checked]);
    }
    public function remove($id) {
        $this->startConditions()
            ->where('id', $id)
            ->update([
                'removed' => 1,
                'watched' => 0
            ]);
    }
}
