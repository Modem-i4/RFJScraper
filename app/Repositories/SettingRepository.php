<?php

namespace App\Repositories;

use App\Models\Setting;
use Illuminate\Support\Facades\App;

class SettingRepository
{
    function startConditions()
    {
        return app(Setting::class);
    }
    public function getAll()
    {
        $perPage = request('perPage');
        $locale = App::currentLocale();
        $columns = [
            'id',
            'alias',
            'value',
            'min_value',
            'max_value',
            'default_value'
        ];

        return $this->startConditions()
            ->where('display', true)
            ->select($columns)
            ->paginate($perPage);
    }

    public function save($id, $newValue)
    {
        $this->startConditions()
            ->where('id', $id)
            ->update(['value' => $newValue]);
    }
}
