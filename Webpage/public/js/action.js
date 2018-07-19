//call this to open the file
//call by running $python3 -m http.server

Papa.parse("http://lvh.me:8000/monthcsvfile.csv", {
    //parameters to set
    download: true,
    header: true,

    complete: function(results) {
        //var data = results.data.sort((a, b) => b.frequency - a.frequency)
        //                       .map(({letter, frequency}) => ({name: letter, value: frequency}));

        var data = results.data.map(({date, messagecount}) => ({name: date, value: messagecount}));

        console.log(data);

        var margin = ({top: 20, right: 0, bottom: 30, left: 40});

        var height = 500;
    
        var width = 1200;
    
        var x = d3.scaleBand()
            .domain(data.map(d => d.name))
            .range([margin.left, width - margin.right])
            .padding(0.1);
    
        var y = d3.scaleLinear()
            .domain([0, d3.max(data, d => parseInt(d.value))]).nice()
            .range([height - margin.bottom, margin.top]);
    
        var xAxis = g => g
            .attr("transform", `translate(0,${height - margin.bottom})`)
            .call(d3.axisBottom(x)
                .tickSizeOuter(0));
    
        var yAxis = g => g
            .attr("transform", `translate(${margin.left},0)`)
            .call(d3.axisLeft(y))
            .call(g => g.select(".domain").remove());
    
        const svg = d3.select("body").append("svg")
            .attr('width', width)
            .attr('height', height);
        
        svg.append("g")
            .attr("fill", "steelblue")
        .selectAll("rect").data(data).enter().append("rect")
            .attr("x", d => x(d.name))
            .attr("y", d => y(d.value))
            .attr("height", d => y(0) - y(d.value))
            .attr("width", x.bandwidth());
    
        svg.append("g")
            .call(xAxis);
    
        svg.append("g")
            .call(yAxis);
    
        return svg.node();
    }
}); 

Papa.parse("http://lvh.me:8000/weekcsvfile.csv", {
    //parameters to set
    download: true,
    header: true,

    complete: function(results) {
        //var data = results.data.sort((a, b) => b.frequency - a.frequency)
        //                       .map(({letter, frequency}) => ({name: letter, value: frequency}));

        var data = results.data.map(({date, messagecount}) => ({name: date, value: messagecount}));

        console.log(data);

        var margin = ({top: 20, right: 0, bottom: 30, left: 40});

        var height = 500;
    
        var width = 8700;
    
        var x = d3.scaleBand()
            .domain(data.map(d => d.name))
            .range([margin.left, width - margin.right])
            .padding(0.1);
        
        

        var y = d3.scaleLinear()
            .domain([0, d3.max(data, d => parseInt(d.value))]).nice()
            .range([height - margin.bottom, margin.top]);
    
        var xAxis = g => g
            .attr("transform", `translate(0,${height - margin.bottom})`)
            .call(d3.axisBottom(x)
                .tickSizeOuter(0));
    
        var yAxis = g => g
            .attr("transform", `translate(${margin.left},0)`)
            .call(d3.axisLeft(y))
            .call(g => g.select(".domain").remove());
    
        const svg = d3.select("body").append("svg")
            .attr('width', width)
            .attr('height', height);
        
        svg.append("g")
            .attr("fill", "steelblue")
            .selectAll("rect").data(data).enter().append("rect")
                .attr("x", d => x(d.name))
                .attr("y", d => y(d.value))
                .attr("height", d => y(0) - y(d.value))
                .attr("width", x.bandwidth());

    
        svg.append("g")
            .call(xAxis);
    
        svg.append("g")
            .call(yAxis);
    
        return svg.node();
    }
}); 


//message sent percentage
Papa.parse("http://lvh.me:8000/message_sent_count_csvfile.csv", {
    //parameters to set
    download: true,
    header: true,

    complete: function(results) {
        var user1_name = results.data[0].name;
        var user1_count = results.data[0].count;

        var user2_name = results.data[1].name;
        var user2_count = results.data[1].count;

        //get user 1 percentage of messages sent
        var user1_percentage = (parseInt(user1_count)*100/(parseInt(user1_count)+parseInt(user2_count))).toFixed(2) + "%";

        var user2_percentage = (parseInt(user2_count)*100/(parseInt(user1_count)+parseInt(user2_count))).toFixed(2) + "%";

        //percentage
        {
            //user one
            {
                //write user one name
                var stat_id = $('#ui_box_message_sent_percentage #user_one_name');
                stat_id.children('span').html(user1_name);

                //write into progress bar one span
                var stat_id = $('#ui_box_message_sent_percentage #user_one_stat');
                stat_id.children('span').html(user1_percentage);

                //write to progress bar one
                var progress_bar_one = $('#ui_box_message_sent_percentage #user_one_progress_bar');
                progress_bar_one.width(user1_percentage);
            }

            //user two
            {
                //write user two name
                var stat_id = $('#ui_box_message_sent_percentage #user_two_name');
                stat_id.children('span').html(user2_name);

                //write into progress bar one span
                var stat_id = $('#ui_box_message_sent_percentage #user_two_stat');
                stat_id.children('span').html(user2_percentage);

                //write to progress bar one
                var progress_bar_two = $('#ui_box_message_sent_percentage #user_two_progress_bar');
                progress_bar_two.width(user2_percentage);
            }
        }

        //count
        {
            //user one
            {
                //write user one name
                var stat_id = $('#ui_box_message_sent_count #user_one_name');
                stat_id.children('span').html(user1_name);

                //write into progress bar one span
                var stat_id = $('#ui_box_message_sent_count #user_one_stat');
                stat_id.children('span').html(user1_count);

                //write to progress bar one
                var progress_bar_one = $('#ui_box_message_sent_count #user_one_progress_bar');
                progress_bar_one.width(user1_percentage);
            }

            //user two
            {
                //write user two name
                var stat_id = $('#ui_box_message_sent_count #user_two_name');
                stat_id.children('span').html(user2_name);

                //write into progress bar one span
                var stat_id = $('#ui_box_message_sent_count #user_two_stat');
                stat_id.children('span').html(user2_count);

                //write to progress bar one
                var progress_bar_two = $('#ui_box_message_sent_count #user_two_progress_bar');
                progress_bar_two.width(user2_percentage);
            }
        }
    }
});

//message sent first and last date
Papa.parse("http://lvh.me:8000/message_sent_first_last_date_csvfile.csv", {
    //parameters to set
    download: true,
    header: true,

    complete: function(results) {
        var user1_name = results.data[0].name;
        var user1_date = results.data[0].date;

        console.log(user1_date);

        var user2_name = results.data[1].name;
        var user2_date = results.data[1].date;

        {
            //user one
            {
                //write user one name
                var stat_id = $('#ui_box_first_last_date #user_one_name');
                stat_id.children('span').html(user1_name);

                //write into progress bar one span
                var stat_id = $('#ui_box_first_last_date #user_one_stat');
                stat_id.children('span').html(user1_date);
            }

            //user two
            {
                //write user two name
                var stat_id = $('#ui_box_first_last_date #user_two_name');
                stat_id.children('span').html(user2_name);

                //write into progress bar one span
                var stat_id = $('#ui_box_first_last_date #user_two_stat');
                stat_id.children('span').html(user2_date);
            }
        }
    }
});
