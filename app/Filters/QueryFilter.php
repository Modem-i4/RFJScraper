<?php


namespace App\Filters;


use Illuminate\Database\Query\Builder;
use Illuminate\Http\Request;
use Illuminate\Support\Str;

abstract class QueryFilter
{
    /**
     * @var Builder
     */
    protected $builder;

    /**
     * @var Request
     */
    protected $request;

    /**
     * The default namespace where filters reside.
     *
     * @var string
     */
    protected static $namespace = 'App\\Filters\\';

    /**
     * The attributes that can be searched
     *
     * @var array
     */
    protected $searchable = [];

    /**
     * The attributes that can be sorted
     *
     * @var array
     */
    protected $sortable = [];

    /**
     * The name of the "sortBy" parameter.
     *
     * @var string
     */
    protected $sortBy = 'sortBy';

    /**
     * The name of the "sortDirection" parameter.
     *
     * @var string
     */
    protected $sortDirection = 'sortDirection';    //TODO: Add custom sort(float, numeric, date)

    /**
     * The name of the "search" parameter.
     *
     * @var string
     */
    protected $search = 'search';
    /**
     * The name of the "column search" parameter.
     *
     * @var string
     */
    protected $searches = 'searches';

    public function __construct(Request $request)
    {
        $this->request = $request;
    }

    /**
     * @return array
     */
    public function filters()
    {
        return request()->all();
    }

    public static function filterForModel($modelName)    //TODO: Optimize
    {
        $modelName = Str::after($modelName, 'App\\Models\\');
        $className = static::$namespace.$modelName.'Filter';

        return $className;
    }

    /**
     * @param Builder $builder
     * @return Builder
     */
    public function apply($builder)
    {
        $this->builder = $builder;

        foreach ($this->filters() as $filter => $value) {    // TODO: Refactor
            $filter = $filter.'Filter';
            if(method_exists($this, $filter)) {
                $this->$filter($value);
            }
        }

        $this->search();
        $this->columnSearch();
        $this->sort();
        return $this->builder;
    }


    public function sort()    //TODO: Add protected 'sortable' list, multiple sorting
    {
        if(in_array(request($this->sortBy), $this->sortable)) {
            $field = request($this->sortBy);

            $receivedDirection = Str::lower(request($this->sortDirection));
            $direction = ($receivedDirection == 'desc') ? 'desc' : 'asc';

            $this->builder
                ->orderBy($field, $direction);
        }
    }

    public function search()
    {
        if(request()->has($this->search))    // Якщо запит хоче виконати пошук
        {
            $this->builder->Where(function($query) {
                $searchString = request($this->search);
                foreach ($this->searchable as $field) {
                    $query->orWhere($field, 'like', "%$searchString%");
                }
            });
        }
    }

    public function columnSearch()
    {
        if(request()->has($this->searches))    // Якщо запит хоче виконати пошук
        {
            $searches = json_decode(request($this->searches));
            foreach ($searches as $field => $query) {
                if($query !== '')
                    $this->builder->Where($field, 'like', "%$query%");
            }
        }
    }

}
