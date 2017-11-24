// 设置颜色渐变
function setGradient(){
    var gradient = {};
    var colors = document.querySelectorAll("input[type='color']");
    colors = [].slice.call(colors,0);
    colors.forEach(function(ele){
        gradient[ele.getAttribute("data-key")] = ele.value; 
    });
    heatmapOverlay.setOptions({"gradient":gradient});
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

	document.getElementById("cdate").innerHTML = "当前日期：" + year + "-" + month + "-" + day;
	var startJsonFile = "./json/" + year + month + "/" + day + "_start.json";
	var endJsonFile = "./json/" + year + month + "/" + day + "_end.json";
	plotHeatMap(curDate,startJsonFile,endJsonFile);

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
		plotHeatMap(sDate,startJsonFile,endJsonFile);
	},500);

}

function plotHeatMap(sDate,startJsonFile,endJsonFile){
	map.centerAndZoom(point, zoomSize);
	removeOverlay();

    $.getJSON(startJsonFile, function (data) {
            var points = data;
            heatmapOverlay.setDataSet({data:points,max:countMax});
            //是否显示热力图
            heatmapOverlay.show();
    });

    $.getJSON(endJsonFile, function (data) {
            var points1 = data;
            heatmapOverlay1.setDataSet({data:points1,max:countMax});
            //是否显示热力图
            heatmapOverlay1.show();
    });

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

function hideHeatMap(){
	// map.clearOverlays();   //这种方法不能再次加载热力图
	heatmapOverlay.hide();
}

function plotPath(sDate,pathJsonFile){
	map.centerAndZoom(point_, zoomSize1);
	hideHeatMap();
	removeOverlay();
	// 绘制top10路线	
    $.getJSON(pathJsonFile, function (data) {
            var points = data;
            
    		for(var i=0; i<points.length; i++){
    			var polyline = new BMap.Polyline([
        			new BMap.Point(points[i]['slng'], points[i]['slat']),
        			new BMap.Point(points[i]['elng'], points[i]['elat'])
    			], {strokeColor:"black", strokeWeight:points[i]['count'] / 5, strokeOpacity:1.0});

    			var sPoint = new BMap.Point(points[i]['slng'], points[i]['slat']);
    			var ePoint = new BMap.Point(points[i]['elng'], points[i]['elat']);
    			var marker1 = new BMap.Marker(sPoint);
    			var myIcon = new BMap.Icon("http://api.map.baidu.com/img/markers.png", new BMap.Size(23, 25), {

    // offset: new BMap.Size(10, 25),
    imageOffset: new BMap.Size(0, 0 - 12 * 25)

  });
    			var marker2 = new BMap.Marker(ePoint,{icon: myIcon});

    			lineList[lineList.length] = polyline;//记录要绘制的线
    			pointList[pointList.length] = marker1;
    			pointList[pointList.length] = marker2;

    			map.addOverlay(polyline);
    			map.addOverlay(marker1);
    			map.addOverlay(marker2);
    		}
            // 绘制箭头
            for(var i=0; i<lineList.length; i++){
                arrowLineList[arrowLineList.length] = addArrow(lineList[i],arrowLineLengthRate,Math.PI / 7);//记录绘制的箭头线
            }
    });

	sDate.setDate(sDate.getDate()+1);
}


function addArrow1(polyline,length,angleValue){
	// 使用百度地图自带api的箭头
	var vectorFCArrow = new BMap.Marker(new BMap.Point(point.lng-0.01,point.lat), {
	  // 初始化方向向上的闭合箭头
	  icon: new BMap.Symbol(BMap_Symbol_SHAPE_FORWARD_CLOSED_ARROW, {
	    scale: 2,
	    strokeWeight: 1,
	    rotation: 0,//顺时针旋转30度
	    fillColor: 'red',
	    fillOpacity: 0.8
	  })
	});
	map.addOverlay(vectorFCArrow);
	return vectorFCArrow;
}
/**
     * 在百度地图上给绘制的直线添加箭头
     * @param polyline 直线 var line = new BMap.Polyline([faydPoint,daohdPoint], {strokeColor:"blue", strokeWeight:3, strokeOpacity:0.5});
     * @param length 箭头线的长度 一般是10
     * @param angleValue 箭头与直线之间的角度 一般是Math.PI/7
    	绘制两条直线当做箭头使用，效果不是很好，两边不对称
     */
function addArrow(polyline,length,angleValue){ //绘制箭头的函数
        var linePoint=polyline.getPath();//线的坐标串
        var arrowCount=linePoint.length;
        for(var i =1;i<arrowCount;i++){ //在拐点处绘制箭头
            var pixelStart=map.pointToPixel(linePoint[i-1]);
            var pixelEnd=map.pointToPixel(linePoint[i]);
            var angle=angleValue;//箭头和主线的夹角
            var r=length; // r/Math.sin(angle)代表箭头长度
            var delta=0; //主线斜率，垂直时无斜率
            var param=0; //代码简洁考虑
            var pixelTemX,pixelTemY;//临时点坐标
            var pixelX,pixelY,pixelX1,pixelY1;//箭头两个点
            if(pixelEnd.x-pixelStart.x==0){ //斜率不存在是时
                pixelTemX=pixelEnd.x;
                if(pixelEnd.y>pixelStart.y)
                {
                pixelTemY=pixelEnd.y-r;
                }
                else
                {
                pixelTemY=pixelEnd.y+r;
                }    
                //已知直角三角形两个点坐标及其中一个角，求另外一个点坐标算法
                pixelX=pixelTemX-r*Math.tan(angle); 
                pixelX1=pixelTemX+r*Math.tan(angle);
                pixelY=pixelY1=pixelTemY;
            }
            else  //斜率存在时
            {
                delta=(pixelEnd.y-pixelStart.y)/(pixelEnd.x-pixelStart.x);
                param=Math.sqrt(delta*delta+1);

                if((pixelEnd.x-pixelStart.x)<0) //第二、三象限
                {
                pixelTemX=pixelEnd.x+ r/param;
                pixelTemY=pixelEnd.y+delta*r/param;
                }
                else//第一、四象限
                {
                pixelTemX=pixelEnd.x- r/param;
                pixelTemY=pixelEnd.y-delta*r/param;
                }
                //已知直角三角形两个点坐标及其中一个角，求另外一个点坐标算法
                pixelX=pixelTemX+ Math.tan(angle)*r*delta/param;
                pixelY=pixelTemY-Math.tan(angle)*r/param;

                pixelX1=pixelTemX- Math.tan(angle)*r*delta/param;
                pixelY1=pixelTemY+Math.tan(angle)*r/param;
            }

            var pointArrow=map.pixelToPoint(new BMap.Pixel(pixelX,pixelY));
            var pointArrow1=map.pixelToPoint(new BMap.Pixel(pixelX1,pixelY1));
            var Arrow = new BMap.Polyline([
                pointArrow,
             linePoint[i],
                pointArrow1
            ], {strokeColor:"black", strokeWeight:3, strokeOpacity:1.0});
            map.addOverlay(Arrow);
            return Arrow;
        }
}

function plotCurPath(){
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

	document.getElementById("cdate").innerHTML = "当前日期：" + year + "-" + month + "-" + day;
	var pathJsonFile = "./path_json/" + year + month + "/" + day + "_path.json";
	plotPath(curDate,pathJsonFile);
}

function plotCurPathChange(){
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
	alert("TOP 10路径变化展示开始！");
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
		var pathJsonFile = "./path_json/" + year + month + "/" + day + "_path.json";
		plotPath(sDate,pathJsonFile);
	},500);
}


function removeOverlay(){
	// 清除所有覆盖物（没有热力图）
	// 清除直线
	for(var i=0; i<lineList.length; i++){
            map.removeOverlay(lineList[i]);//清除制定的覆盖物，可以是直线、标注等
    }
	// 清除绘制的箭头
	for(var i=0; i<arrowLineList.length; i++){
            map.removeOverlay(arrowLineList[i]);//清除制定的覆盖物，可以是直线、标注等
    }
    // 清除起始点标记
	for(var i=0; i<pointList.length; i++){
            map.removeOverlay(pointList[i]);//清除制定的覆盖物，可以是直线、标注等
    }

    lineList.length = 0;
    arrowLineList.length = 0; 
    pointList.length = 0;
}