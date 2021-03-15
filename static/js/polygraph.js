new Vue({
    el: '#app',
    data: {
        text: '',
        exit: false,
    },
    methods: {}
});

new Vue({
    el: '#app-1',
    data: {
        documents:[
            {title:'Doc1'},
            {title:'Doc1'},
            {title:'Doc1'},
            {title:'Doc1'}
        ],
        selectedDocuments:[],
        text: '',
        load: false,
    },
    methods: {
        removeElement: function (index) {
            this.selectedDocuments.splice(index, 1);
          }
    }
});