/**
 * Created by yi on 2018/7/18.
 */
(function () {
    var json_url = null;

    String.prototype.format = function (kwargs) {
        //this: ' {age}-{name}'
        //kwargs: {'age':18,'name':'zhaoziyi'}
        var param = /\{(\w+)\}/g;
        var ret = this.replace(param, function (m, n) {
            //m:{age} {name}
            //n:age name
            //这个replace是使用第二个参数function返回值替换掉匹配的
            return kwargs[n]
        });
        return ret;
    };

    function initTable() {
        var page_num = $('.table').attr('page-num');
        init(page_num);
    }

    function init(page_num) {
        bindCheckAll();
        bindCheckReverse();
        bindEditMode();
        bindCheckBox();
        bindCancel();
        bindSave();

        var p = '?p=' + page_num;
        //通过ajax获取数据数据
        $.ajax({
            ///backend/index-json
            url: json_url + p,
            type: 'GET',
            dataType: 'JSON',
            success: function (arg) {
                //console.log(arg)
                initGlobalVal(arg['global_dict']);
                initHeader(arg['table_config']);
                initBody(arg['table_config'], arg['data_list']);
                initPage(arg['page_str']);
            }
        })
    }

    function initGlobalVal(gloabl_dict) {
        // {'sex_choices':{1: '男', 2: '女'},'status_choice':{1:1}}}
        $.each(gloabl_dict, function (k, v) {
            window[k] = v;
        });
    }

    function initHeader(table_config) {
        var $table_header = $('#table-header');
        var tr = document.createElement('tr');
        $.each(table_config, function (index, dict) {
            if (dict['display']) {
                var th = document.createElement('th');
                th.innerHTML = dict['title'];
                $(tr).append(th);
            }
        });
        $table_header.append(tr);
    }

    function initBody(table_config, data_list) {
        var $table_body = $('#table-body');
        $.each(data_list, function (i, row) {
            var tr = document.createElement('tr');
            // 设置row-id属性，为了更新数据用。一行代表一条数据。
            tr.setAttribute('row-id', row['id']);
            //{id: 1, username: "zhaoziyi", password: "freedom", sex: 1, age: 13, …}

            $.each(table_config, function (index, dict) {
                if (dict['display']) {
                    var content = dict['text']['content'];
                    var format_dict = dict['text']['kwargs'];
                    var attr_dict = dict['attrs'];
                    // {'content': '{n}', 'kwargs': {'n': '@password','m':'@xxx'}

                    //遍历内容字典,得出格式化字典kwargs
                    //  //kwargs: {'age':18,'name':'zhaoziyi'}
                    var kwargs = {};
                    $.each(format_dict, function (k, v) {
                        //k: 'n',v: '@password'
                        if (v.substr(0, 2) == '@@') {
                            var key = dict['field'];
                            var row_data = row[key];
                            var global_name = v.substring(2, v.length);
                            kwargs[k] = window[global_name][row_data];
                        }
                        else if (v[0] == '@') {
                            var key = v.substring(1, v.length);
                            kwargs[k] = row[key];
                        }
                    });
                    var text = content.format(kwargs);
                    var td = document.createElement('td');
                    td.innerHTML = text;
                    //设置属性
                    //这个name属性是必须存在的，为了更新数据
                    td.setAttribute('name', dict['field']);
                    $.each(attr_dict, function (k, v) {
                        if (v[0] == '@') {
                            var key = v.substring(1, v.length);
                            v = row[key]
                        }
                        td.setAttribute(k, v)
                    });
                    $(tr).append(td);
                }
            });
            $table_body.append(tr);
        })
    }

    function bindCheckAll() {
        $('#idCheckAll').click(function () {
            var flag = $(this).hasClass('btn-warning');
            if (flag) {
                $('#table-body').find(':checkbox').each(function () {
                    $(this).prop('checked', false);
                })
                $(this).removeClass('btn-warning');
            }
            else {
                $('#table-body').find(':checkbox').each(function () {
                    $(this).prop('checked', true);
                })
                $(this).addClass('btn-warning');
            }
        });
    }

    function isCheckAll() {
        //当手动把钩子打满后，全选按钮自动变色
        var i = 0;
        var $objs = $('#table-body').find(':checkbox')
        $objs.each(function () {
            if ($(this).prop('checked')) {
                ++i;
            }
        });
        if ($objs.length == i) {
            $('#idCheckAll').addClass('btn-warning');
        }
        else {
            $('#idCheckAll').removeClass('btn-warning');
        }
    }

    function bindCheckBox() {
        $('#table-body').on('change', ':checkbox', function () {
            var flag = $('#idEditMode').hasClass('btn-warning');
            var isCheck = $(this).prop('checked');
            var $tr = $(this).parent().parent();
            if (flag) {
                if (isCheck) {
                    trIntoEditMode($tr);
                } else {
                    trOutEditMode($tr);
                }
            }
            isCheckAll();
        });
    }

    function bindCheckReverse() {
        $('#idCheckReverse').click(function () {
            var $objs = $('#table-body').find(':checkbox')
            $objs.each(function () {
                if ($(this).prop('checked')) {
                    $(this).prop('checked', false);
                }
                else {
                    $(this).prop('checked', true);
                }
            });
            isCheckAll();
        });
    }

    function bindEditMode() {
        $('#idEditMode').click(function () {
            var flag = $(this).hasClass('btn-warning');
            if (flag) {
                //退出编辑模式
                $(this).html('进入编辑模式');
                $(this).removeClass('btn-warning');
                $('#table-body').find(':checkbox').each(function () {
                    if ($(this).prop('checked')) {
                        var $tr = $(this).parent().parent();
                        //调用封装方法
                        trOutEditMode($tr);
                    }
                });
            }
            else {
                //进入编辑模式
                $(this).html('退出编辑模式');
                $(this).addClass('btn-warning');
                //1.找出所有checkbox,让其所在行高亮
                $('#table-body').find(':checkbox').each(function () {
                    if ($(this).prop('checked')) {
                        var $tr = $(this).parent().parent();
                        //调用封装方法
                        trIntoEditMode($tr);
                    }
                });
            }
        });
    }

    function trIntoEditMode($tr) {
        //1.找出所有checkbox,让其所在行高亮
        $tr.addClass('success');
        //2.增加has-edit属性，标记这行已经被编辑过来
        $tr.attr('has-edit', true);
        //遍历$tr的子元素,生成对应的input框
        $.each($tr.children(), function (index, obj) {
            var edit_enable = $(obj).attr('edit-enable');
            var edit_type = $(obj).attr('edit-type');
            //坑，没属性返回undefine，有属性返回字符串版的true,或者False,序列化过来就这模样？
            if (edit_enable == 'true') {
                var input = null;
                if (edit_type == 'input') {
                    input = document.createElement('input');
                    input.className = 'form-contorl';
                    $(input).val($(obj).html());
                }
                else if (edit_type == 'select') {
                    var global_name = $(obj).attr('global-name');
                    input = document.createElement('select');
                    input.className = 'form-contorl';
                    $.each(window[global_name], function (k, v) {
                        // {1: '男', 2: '女'}
                        var option = document.createElement('option');
                        option.setAttribute('value', k);
                        option.innerHTML = v;
                        $(input).append(option);
                    });

                    $(input).val($(obj).attr('origin'));
                }
                $(obj).html(input);
            }
        });
    }

    function trOutEditMode($tr) {
        $tr.removeClass('success');

        $.each($tr.children(), function (index, obj) {
            var edit_enable = $(obj).attr('edit-enable');
            var edit_type = $(obj).attr('edit-type');
            if (edit_enable == 'true') {
                var text = null;
                var new_val = null;
                if (edit_type == 'input') {
                    var $input = $(obj).children().first();
                    text = $input.val();
                    new_val = $input.val();
                }
                else if (edit_type == 'select') {
                    var $sel = $(obj).children().first();
                    text = $sel[0].selectedOptions[0].innerHTML;
                    //用属性记录新值
                    new_val = $sel.val();
                }
                $(obj).attr('new-val', new_val);
                $(obj).html(text);
            }
        });
    }

    function bindCancel() {
        $('#idCancel').click(function () {
            var flag = $('#idEditMode').hasClass('btn-warning');
            if (flag) {
                var $checkboxs = $('#table-body').find(':checkbox');
                $checkboxs.each(function (i, checkbox) {
                    if ($(this).prop('checked')) {
                        var $tr = $(this).parent().parent();
                        $.each($tr.children(), function (index, td) {
                            var edit_enable = $(td).attr('edit-enable');
                            if (edit_enable) {
                                var origin = $(td).attr('origin');
                                $(td).children().first().val(origin);
                            }
                        });
                    }
                });
            }
        });
    }

    function bindSave() {
        $('#idSave').click(function () {
            var flag = $('#idEditMode').hasClass('btn-warning');
            if (flag) {
                alert('请先退出编辑模式');
                return;
            }

            var data_list = [];
            $('#table-body').find('tr[has-edit="true"]').each(function () {
                var $tr = $(this);
                var tmp_dict = {};
                $tr.children('[edit-enable="true"]').each(function () {
                    var name = $(this).attr('name');
                    var origin = $(this).attr('origin');
                    var new_val = $(this).attr('new-val');
                    if (origin != new_val) {
                        tmp_dict[name] = new_val
                    }
                });
                //js中没有判断字典为空的方法，只有调用jquery的isEmptyObject
                if (!$.isEmptyObject(tmp_dict)) {
                    tmp_dict['id'] = $tr.attr('row-id');
                    data_list.push(tmp_dict);
                }
                console.log(data_list)
            });
            //发送ajax
            $.ajax({
                url: json_url,
                type: 'POST',
                dataType: 'JSON',
                data: JSON.stringify(data_list),
                success: function (arg) {
                    console.log(arg)
                    alert(arg['msg']);
                    if (arg['status']) {
                        window.location.reload();
                    }
                }
            })


        })
    }

    function initPage(page_str) {
        var ul = document.createElement('ul');
        ul.className = "pagination pull-right";
        ul.innerHTML = page_str;
        $('.footer').append(ul);
    }

    jQuery.extend({
        'initTable': function (url) {
            json_url = url;
            initTable();
        }
    });

})();