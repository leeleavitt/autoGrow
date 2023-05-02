class light_button_class {
    
    constructor(){
        this.data_grabber()
        this.light_state()
    }

    light_button_maker() {
        let that = this

        d3.select('body')
            .append('div')
            .attr('id', 'light_override_button_box')

        let buttons = d3.select('#light_override_button_box')
        buttons.text('Light override').append('br')
            
        buttons.append('button')
            .attr('id', 'lightButton')
            .attr('class', 'btn btn-primary btn-sm clustButton')
            .attr('data-toggle', 'button')
            .attr('class', this.lightclass)
            .text(this.lightswitch)
            .on('click', d => that.toggler());

        d3.select('body')
            .append('div')
            .append('form')
            .attr('id', 'light_timer')

        var timer = d3.select('#light_timer')
        timer.text('Light Timer')
            .append('br')
        
        timer.append('text').text('Light On')
        timer.append('br')
        timer.append('input')
            .attr('id', 'lightOn')
        timer.append('br')
        
        timer.append('text').text('Light Off')
        timer.append('br')
        timer.append('input')
            .attr('id', 'lightOff')

    };

    light_state() {
        /**
         * Function to toggle the button
         */
        let previous_class = this.lightclass
        if(this.data.lightOnOverride == 1){
            this.lightswitch = 'On'
            this.lightclass = 'switch-on'
        }else{
            this.lightswitch = 'Off'
            this.lightclass = 'switch-off'
        } 

        d3.select('#lightButton')
            .text(this.lightswitch)
            .classed(previous_class, false)
            .classed(this.lightclass, true)

    }
    
    toggler() {
        if(this.data.lightOnOverride == 1){
            this.data.lightOnOverride = 0
        }else{
            this.data.lightOnOverride = 1
        }
        this.light_state()
        this.data_sender('lightOnOverride')
    }

    data_grabber() {
        /**
         * Function to collect data from the flask server
         */

        let that = this
        $.ajax({
            url : '/post_python_data_to_web',
            dataType : 'json',
            contentType: 'application/json',
            type : 'POST',
            success : function(data){
               that.data = data
            },
            async : false
        });
    };

    data_sender(key){
        let entry_loc = Object.keys(light_buttons.data).findIndex(p => p == key)
        let to_pass = Object.entries(light_buttons.data)[entry_loc]

        var data_to_pass = {}
        data_to_pass[to_pass[0]] = to_pass[1]
        console.log(data_to_pass)

        $.ajax({
            url : '/post_python_data_from_sever', 
            type : 'POST', 
            dataType: 'json',
            contentType: 'application/json',
            data : JSON.stringify(data_to_pass)
        })
    }

};

let light_buttons = new light_button_class();
light_buttons.light_button_maker();

