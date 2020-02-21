
ORDER_COMPLETED_MAIL_TEMPLATE = '''
Dear {{first_name}} {{last_name}}
<br>
<br>
<br>
<br>
<h2>Your order num {{order_num}} is completed.</h2>
<br>
<table>
    <thead>
        <tr>
            <th scope="col">#</th>
            <th scope="col">Name</th>
            <th scope="col">Option</th>
            <th scope="col">Unit price</th>
            <th scope="col">Numbers</th>
            <th scope="col">Extras</th>
        </tr>
    </thead>
    <tbody>
        {% for option in order_details %}
        <tr>
            <td>{{loop.index}}</td>
            <td>{{option.name}}</td>
            <td>{{option.option}}</td>
            <td>{{option.price}}</td>
            <td>{{option.num}}</td>
            <td>
                {% for extra in option.extras %}
                <p>{{extra.name}}&nbsp;&nbsp;&nbsp;cost:&nbsp;{{extra.cost}}&nbsp;&nbsp;&nbsp;num:&nbsp;{{extra.num}}</p>
                {% endfor %}
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
<br>
<h4>Total   {{amount}}</h4>
<br>
<br>
<br>
<br>

BR,<br>
Pizza Man {{admin_name}}
'''