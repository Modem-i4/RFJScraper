<?php


namespace App\Traits;


use App\Filters\QueryFilter;

trait Filterable
{
    /**
     * @param $query
     * @return mixed
     */
    public function scopeFilter($query)
    {
        return $this->getFilterInstance()->apply($query);
    }

    public function getFilterInstance()
    {
        $filter = static::newFilter() ?: QueryFilter::filterForModel(get_called_class());

        return app($filter);
    }

    /**
     * Create a new filter instance for the model.
     *
     * @return string|void
     */
    protected static function newFilter()
    {
        //
    }
}
