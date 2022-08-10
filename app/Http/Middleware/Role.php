<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class Role
{
    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle(Request $request, Closure $next, $role)
    {
        if(Auth::user() != null) {
            if(!Auth::user()->hasRole($role)) {
                return response()->view('welcome');
            }
            return $next($request);
        }
        else {
            return redirect('login');
        }
    }
}
