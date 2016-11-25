var app = angular.module('app',
    ['angularUtils.directives.dirPagination'],
    function ($interpolateProvider) {
        $interpolateProvider.startSymbol('<%');
        $interpolateProvider.endSymbol('%>');
    }
);
app.factory('Person', ['$http', function ($http) {
    return {
        getList: function (q, page, limit, sort, reverse) {
            return $http({
                method: 'GET',
                url: '/api/search_persons_eloquent',
                params: {
                    "q": q,
                    "page": page,
                    "limit": limit,
                    "sort": sort,
                    "reverse": reverse
                }
            });
        }
    }
}]);
app.controller('PersonsListCtrl', ['$scope','$http', 'Person', function ($scope, $http, Person) {
    $scope.persons = [];
    $scope.currentPage = 1;
    $scope.pageSize = 10;
    $scope.totalPersons = 0;
    $scope.q = '';
    $scope.sort = 'created_at';
    $scope.reverse = false;

    $scope.getPersons = function (page) {
        var rev = $scope.reverse ? 'ASC' : 'DESC';
        Person.getList($scope.q,page,$scope.pageSize,$scope.sort, rev)
            .success(function (response) {
                $scope.totalPersons = response.count;
                $scope.persons = response.data;
            })
            .error(function (errors) {
               // console.log(errors);
            });
    };

    $scope.ChangeSort = function(column) {
        if (column === $scope.sort) {
            $scope.reverse = !$scope.reverse;
        } else {
            $scope.sort = column;
            $scope.reverse = false;
        }
        $scope.getPersons($scope.currentPage);
    };

    $scope.getPersons($scope.currentPage);
}]);