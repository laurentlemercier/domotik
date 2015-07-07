(function (angular) {
  var app = angular.module("domotikApp", ['nvd3ChartDirectives']);

  app.service('domotikSrv', function ($http) {

    return({
      last: last
    });

    function last(time, type) {
      return $http.get("api/last/" + time + "/" + type);
    }

  });

  app.controller('domotikIndexCtrl', function($scope, $interval, domotikSrv){
      domotikSrv.last("24h", "temp").then(function(response) {
        $scope.twenty_four_hours_temp = response.data;
      });

      domotikSrv.last("24h", "watt").then(function(response) {
        $scope.twenty_four_hours_watt = response.data;
      });

      function update() {
        domotikSrv.last("20s", "temp").then(function(response) {
          response.data.forEach(function(e1) {
            var d = $scope.twenty_four_hours_temp;
            d.forEach(function(e2) {
                if (e2.key == e1.key) {
                  e1.values.forEach(function(e3) {
                    e2.values.push(e3);
                    $scope.last_temp = e1.key + " " + e3[1] + "°c";
                  });
                }
            });
            $scope.twenty_four_hours_temp = d;
          });
        });
        domotikSrv.last("20s", "watt").then(function(response) {
          response.data.forEach(function(e1) {
            var d = $scope.twenty_four_hours_watt;
            d.forEach(function(e2) {
                if (e2.key == e1.key) {
                  e1.values.forEach(function(e3) {
                    e2.values.push(e3);
                    $scope.last_watt = e1.key + " " + e3[1] + "W";
                  });
                }
            });
            $scope.twenty_four_hours_watt = d;
          });
        })
      }
      setInterval(function() {$scope.$apply(update);}, 20000 /* 20S */);

      $scope.xAxisTickFormat_Date_Format = function() {
        return function(d) {
          return d3.time.format('%x')(new Date(d * 1000));
        }
      }
      $scope.xAxisTickFormat_Time_Format = function() {
        return function(d) {
          return d3.time.format('%X')(new Date(d * 1000));
        }
      }
      $scope.yAxisTickFormat_Temp_Format = function() {
        return function(d) {
          return d + "°c";
        }
      }
      $scope.yAxisTickFormat_Watt_Format = function() {
        return function(d) {
          return d + "W";
        }
      }
  });
}(angular));
