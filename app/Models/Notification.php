<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use App\Traits\Filterable;

class Notification extends Model
{
    use HasFactory, Filterable;
    protected $casts = [
        ];
    public $timestamps = false;
}
