class buttuns {
    
    constructor(){
        this.data_grabber()
        console.log(this)
        //this.light_state()
        // this.light_state()
    }

    data_grabber() {
        /**
         * Function to collect data from the flask server
         */
        let that = this
        that.data = data_collector()
    };


    light_state() {
        /**
         * Function to toggle the button
         */
        console.log(this.data)
    }


};

function data_collector(){
    return 'hi'
}

let light_buttuns = new buttuns();


