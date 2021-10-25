const grid = {
    view: "datatable",
    columns: [
        {id: "item", editor: "text", header: "Item", fillspace: true},
        {id: "count_item", editor: "number", header: "Count"},
        {id: "price_item", editor: "number", header: "Price"},
        {id: "discount", editor: "number", header: "Discount"},
        {id: "total", editor: "number", header: "Total"},
        {id: "status", editor: "text", header: "Status"},
        {id: "action", editor: "text", header: "Action"}
    ],
    editable: true,
    autoheight: true,
    autowidth: true,
};

webix.ready(function () {
    webix.ui({
        padding: 15,
        cols: [
            {
                rows: [
                    grid
                ]
            }
        ]
    });

});