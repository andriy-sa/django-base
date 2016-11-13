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
                url: '/api/search_persons',
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
        Person.getList($scope.q,page,$scope.pageSize,$scope.sort,$scope.reverse)
            .success(function (response) {
               console.log(response)
            })
            .error(function (errors) {
               // console.log(errors);
            });
    };

    $scope.getPersons($scope.currentPage);
}]);