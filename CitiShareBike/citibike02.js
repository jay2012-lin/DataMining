(function defaultF(){
	// 初始化时加载
	InitHeatMap();
})();

function InitHeatMap(){
	// 初始化热力图
	var curDate = document.getElementById("in_date").value;  //2017-07-01
	// alert(curDate);
	var dateList = curDate.split("-");
	var year = dateList[0];
	var month = dateList[1];
	var day = dateList[2];
	// new Date中月份是从0开始索引的:3 => 2
	curDate = new Date(year,month-1,day);
	var minDate = new Date(2013,6,01);
	var maxDate = new Date(2017,2,31);
	// alert(curDate+minDate+maxDate)
	if(curDate < minDate || curDate > maxDate){
		alert("您输入的日期没有数据，请输入2013/07/01~2017/03/31之间的日期！");
		return false;
	}
	var startJsonFile = "./json/" + year + month + "/" + day + "_start.json"
	var endJsonFile = "./json/" + year + month + "/" + day + "_end.json"
	var dom = document.getElementById("container_left");
          var myChart = echarts.init(dom);
          var app = {};
          option = null;
          app.title = '热力图与百度地图扩展';

          $.get(startJsonFile, function (data) {

              var points = [].concat.apply([], data.map(function (track) {
                  return track.map(function (seg) {
                      return seg.coord.concat([seg.weight]);
                  });
              }));
              // alert(points);
              myChart.setOption(option = {
                  animation: false,
                  bmap: {
                  	// 经纬度数据：经度在前，维度在后
                  	  center: [-73.990311,40.720438],//纽约
                      zoom: 13,
                      roam: true
                  },
                  visualMap: {
                      show: false,
                      top: 'top',
                      min: 0,
                      max: 150,
                      seriesIndex: 0,
                      calculable: true,
                      inRange: {
                          color: ['lightskyblue', 'blue', 'yellow', 'orange', 'red']
                      }
                  },
                  series: [{
                      type: 'heatmap',
                      coordinateSystem: 'bmap',
                      data: points,
                      pointSize: 8,
                      blurSize: 8
                  }]
              });
              if (!app.inNode) {
                  // 添加百度地图插件
                  var bmap = myChart.getModel().getComponent('bmap').getBMap();
                  bmap.addControl(new BMap.MapTypeControl());
              }
          });
          if (option && typeof option === "object") {
              myChart.setOption(option, true);
          }
 			// 设置右边的格式
          var dom1 = document.getElementById("container_right");
          var myChart1 = echarts.init(dom1);
          var app1 = {};
          option1 = null;
          app.title = '热力图与百度地图扩展1';

          $.get(endJsonFile, function (data) {

              var points1 = [].concat.apply([], data.map(function (track) {
                  return track.map(function (seg) {
                      return seg.coord.concat([seg.weight]);
                  });
              }));
              // alert(points);
              myChart1.setOption(option = {
                  animation: false,
                  bmap: {
                    // 经纬度数据：经度在前，维度在后
                      center: [-73.990311,40.720438],//纽约
                      zoom: 13,
                      roam: true
                  },
                  visualMap: {
                      show: false,
                      top: 'top',
                      min: 0,
                      max: 150,
                      seriesIndex: 0,
                      calculable: true,
                      inRange: {
                          color: ['lightskyblue', 'blue', 'yellow', 'orange', 'red']
                      }
                  },
                  series: [{
                      type: 'heatmap',
                      coordinateSystem: 'bmap',
                      data: points1,
                      pointSize: 8,
                      blurSize: 8
                  }]
              });
              if (!app1.inNode) {
                  // 添加百度地图插件
                  var bmap = myChart1.getModel().getComponent('bmap').getBMap();
                  bmap.addControl(new BMap.MapTypeControl());
              }
          });
          if (option1 && typeof option1 === "object") {
              myChart1.setOption(option1, true);
          }

}

function getCurDateHeat(){
	// 生成当前热力图
	var curDate = document.getElementById("in_date").value;  //2017-07-01
	// alert(curDate);
	var dateList = curDate.split("-");
	var year = dateList[0];
	var month = dateList[1];
	var day = dateList[2];
	// new Date中月份是从0开始索引的:3 => 2
	curDate = new Date(year,month-1,day);
	var minDate = new Date(2013,6,01);
	var maxDate = new Date(2017,2,31);
	// alert(curDate+minDate+maxDate)
	if(curDate < minDate || curDate > maxDate){
		alert("您输入的日期没有数据，请输入2013/07/01~2017/03/31之间的日期！");
		return false;
	}
	plotHeatMap(curDate);	

}

function heatChange(){
	// if(getHeatChange() === false){
	// 	alert("热力图变化展示结束！");
	// }
	f(getHeatChange);
	alert("结束");
}

function f(f1){
	f1();
}
function getHeatChange(){
	// 生成时间段内的热力图变化
	var sDate = document.getElementById("in_date").value;  //2017-07-01
	var eDate = document.getElementById("out_date").value;
	// alert(curDate);
	var sList = sDate.split("-");
	var eList = eDate.split("-");
	var year = sList[0];
	var month = sList[1];
	var day = sList[2];

	var year_ = eList[0];
	var month_ = eList[1];
	var day_ = eList[2];
	// new Date中月份是从0开始索引的:3 => 2
	sDate = new Date(year,month-1,day);
	eDate = new Date(year_,month_-1,day_);
	var minDate = new Date(2013,6,01);
	var maxDate = new Date(2017,2,31);
	// alert(curDate+minDate+maxDate)
	if(sDate > eDate){
		alert("您输入的时间段不合理，请保证截止日期晚于开始日期！");
		return false;
	}
	if(sDate < minDate || sDate > maxDate){
		alert("您输入的开始日期没有数据，请输入2013/07/01~2017/03/31之间的日期！");
		return false;
	}
	if(eDate < minDate || eDate > maxDate){
		alert("您输入的截止日期没有数据，请输入2013/07/01~2017/03/31之间的日期！");
		return false;
	}
	alert("热力图变化展示开始！");
	// 实现热力变化
	cMap = setInterval(function(){
		// alert(sDate+eDate);
		if(sDate > eDate){
			clearInterval(cMap);    //清除定时器
			return false;
		}
		year = sDate.getFullYear();
		month = sDate.getMonth() + 1;
		day = sDate.getDate();

		month = month + "";
		day = day + "";
		if(month.length == 1){
			month = "0" + month;
		}
		if(day.length == 1){
			day = "0" + day;
		}
		var dateStr = "" + year + "-" + month + "-" + day;
		document.getElementById("in_date").value = dateStr;
		document.getElementById("cdate").innerHTML = "当前日期：" + dateStr;
		var startJsonFile = "./json/" + year + month + "/" + day + "_start.json";
		var endJsonFile = "./json/" + year + month + "/" + day + "_end.json";
		var dom = document.getElementById("container_left");
	          var myChart;
	          // there is a chart instance already initialized on the dom
	          // 因为已经存在热力图，所以不需要初始化init,否则报上面的错。
	          myChart = echarts.getInstanceByDom(document.getElementById("container_left"));
	          var app = {};
	          option = null;
	          app.title = '热力图与百度地图扩展';

	          $.get(startJsonFile, function (data) {

	              var points = [].concat.apply([], data.map(function (track) {
	                  return track.map(function (seg) {
	                      return seg.coord.concat([seg.weight]);
	                  });
	              }));
	              // alert(points);
	              myChart.setOption(option = {
	                  animation: false,
	                  bmap: {
	                  	// 经纬度数据：经度在前，维度在后
	                  	  center: [-73.990311,40.720438],//纽约
	                      zoom: 13,
	                      roam: true
	                  },
	                  visualMap: {
	                      show: false,
	                      top: 'top',
	                      min: 0,
	                      max: 150,
	                      seriesIndex: 0,
	                      calculable: true,
	                      inRange: {
	                          color: ['lightskyblue', 'blue', 'yellow', 'orange', 'red']
	                      }
	                  },
	                  series: [{
	                      type: 'heatmap',
	                      coordinateSystem: 'bmap',
	                      data: points,
	                      pointSize: 8,
	                      blurSize: 8
	                  }]
	              });
	              if (!app.inNode) {
	                  // 添加百度地图插件
	                  var bmap = myChart.getModel().getComponent('bmap').getBMap();
	                  bmap.addControl(new BMap.MapTypeControl());
	              }
	          });
	          if (option && typeof option === "object") {
	              myChart.setOption(option, true);
	          }
	 			// 设置右边的格式
	          var dom1 = document.getElementById("container_right");
	          var myChart1;
	          myChart1 = echarts.getInstanceByDom(document.getElementById("container_right"));
	          var app1 = {};
	          option1 = null;
	          app.title = '热力图与百度地图扩展1';

	          $.get(endJsonFile, function (data) {

	              var points1 = [].concat.apply([], data.map(function (track) {
	                  return track.map(function (seg) {
	                      return seg.coord.concat([seg.weight]);
	                  });
	              }));
	              // alert(points);
	              myChart1.setOption(option = {
	                  animation: false,
	                  bmap: {
	                    // 经纬度数据：经度在前，维度在后
	                      center: [-73.990311,40.720438],//纽约
	                      zoom: 13,
	                      roam: true
	                  },
	                  visualMap: {
	                      show: false,
	                      top: 'top',
	                      min: 0,
	                      max: 150,
	                      seriesIndex: 0,
	                      calculable: true,
	                      inRange: {
	                          color: ['lightskyblue', 'blue', 'yellow', 'orange', 'red']
	                      }
	                  },
	                  series: [{
	                      type: 'heatmap',
	                      coordinateSystem: 'bmap',
	                      data: points1,
	                      pointSize: 8,
	                      blurSize: 8
	                  }]
	              });
	              if (!app1.inNode) {
	                  // 添加百度地图插件
	                  var bmap = myChart1.getModel().getComponent('bmap').getBMap();
	                  bmap.addControl(new BMap.MapTypeControl());
	              }
	          });
	          if (option1 && typeof option1 === "object") {
	              myChart1.setOption(option1, true);
	          }
		sDate.setDate(sDate.getDate()+1);
	},500);

}

function plotHeatMap(sDate){
	year = sDate.getFullYear();
		month = sDate.getMonth() + 1;
		day = sDate.getDate();

		month = month + "";
		day = day + "";
		if(month.length == 1){
			month = "0" + month;
		}
		if(day.length == 1){
			day = "0" + day;
		}
		var dateStr = "" + year + "-" + month + "-" + day;
		document.getElementById("in_date").value = dateStr;
		document.getElementById("cdate").innerHTML = "当前日期：" + dateStr;
		var startJsonFile = "./json/" + year + month + "/" + day + "_start.json";
		var endJsonFile = "./json/" + year + month + "/" + day + "_end.json";
		var dom = document.getElementById("container_left");
	          var myChart;
	          // there is a chart instance already initialized on the dom
	          // 因为已经存在热力图，所以不需要初始化init,否则报上面的错。
	          myChart = echarts.getInstanceByDom(document.getElementById("container_left"));
	          var app = {};
	          option = null;
	          app.title = '热力图与百度地图扩展';

	          $.get(startJsonFile, function (data) {

	              var points = [].concat.apply([], data.map(function (track) {
	                  return track.map(function (seg) {
	                      return seg.coord.concat([seg.weight]);
	                  });
	              }));
	              // alert(points);
	              myChart.setOption(option = {
	                  animation: false,
	                  bmap: {
	                  	// 经纬度数据：经度在前，维度在后
	                  	  center: [-73.990311,40.720438],//纽约
	                      zoom: 13,
	                      roam: true
	                  },
	                  visualMap: {
	                      show: false,
	                      top: 'top',
	                      min: 0,
	                      max: 150,
	                      seriesIndex: 0,
	                      calculable: true,
	                      inRange: {
	                          color: ['lightskyblue', 'blue', 'yellow', 'orange', 'red']
	                      }
	                  },
	                  series: [{
	                      type: 'heatmap',
	                      coordinateSystem: 'bmap',
	                      data: points,
	                      pointSize: 8,
	                      blurSize: 8
	                  }]
	              });
	              if (!app.inNode) {
	                  // 添加百度地图插件
	                  var bmap = myChart.getModel().getComponent('bmap').getBMap();
	                  bmap.addControl(new BMap.MapTypeControl());
	              }
	          });
	          if (option && typeof option === "object") {
	              myChart.setOption(option, true);
	          }
	 			// 设置右边的格式
	          var dom1 = document.getElementById("container_right");
	          var myChart1;
	          myChart1 = echarts.getInstanceByDom(document.getElementById("container_right"));
	          var app1 = {};
	          option1 = null;
	          app.title = '热力图与百度地图扩展1';

	          $.get(endJsonFile, function (data) {

	              var points1 = [].concat.apply([], data.map(function (track) {
	                  return track.map(function (seg) {
	                      return seg.coord.concat([seg.weight]);
	                  });
	              }));
	              // alert(points);
	              myChart1.setOption(option = {
	                  animation: false,
	                  bmap: {
	                    // 经纬度数据：经度在前，维度在后
	                      center: [-73.990311,40.720438],//纽约
	                      zoom: 13,
	                      roam: true
	                  },
	                  visualMap: {
	                      show: false,
	                      top: 'top',
	                      min: 0,
	                      max: 150,
	                      seriesIndex: 0,
	                      calculable: true,
	                      inRange: {
	                          color: ['lightskyblue', 'blue', 'yellow', 'orange', 'red']
	                      }
	                  },
	                  series: [{
	                      type: 'heatmap',
	                      coordinateSystem: 'bmap',
	                      data: points1,
	                      pointSize: 8,
	                      blurSize: 8
	                  }]
	              });
	              if (!app1.inNode) {
	                  // 添加百度地图插件
	                  var bmap = myChart1.getModel().getComponent('bmap').getBMap();
	                  bmap.addControl(new BMap.MapTypeControl());
	              }
	          });
	          if (option1 && typeof option1 === "object") {
	              myChart1.setOption(option1, true);
	          }
	sDate.setDate(sDate.getDate()+1);
}


// 以下是js sleep的函数，但是效果不好
function sleep(n){
    var start=new Date().getTime();
    while(true) if(new Date().getTime()-start>n) break;
}

function sleep1(milliSeconds){
    var resource;
    var response;
    if(typeof ActiveXObject == 'undefined'){
        resource = new XMLHttpRequest();
    }
    else{
        // IE
        resource = new ActiveXObject("Microsoft.XMLHTTP");
    }
 
    try{
        resource.open('GET', 'sleep.php?milliSeconds=' + milliSeconds, false);
        resource.send(null);
        response = resource.responseText; // JavaScript waits for response
    }
    catch(e){
        alert(e);
    }
     
    return true;
}