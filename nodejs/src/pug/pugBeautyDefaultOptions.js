/*
 * @Author: CPS
 * @Date:   2020-08-20 10:26:14
 * @Last Modified by: CPS
 * @Last Modified time: 2021-04-06 23:58:43
 * https://github.com/prettier/plugin-pug#usage
 */

module.exports = {
  semi: true, //使用分号结尾
  parser: "pug",

  pugBracketSpacing: true,

  // 单行属性换行的最大字符限制
  pugPrintWidth: 80,

  // 使用单引号
  pugSingleQuote: true,

  // 缩进
  // pugTabWidth:2,
  //
  // 缩进使用 tab
  // pugUseTabs:false,

  // pugArrowParens: "<>",

  // 是否添加逗号分隔
  // always    - button(type="submit", (click)="play()", disabled)
  // as-needed - button(type="submit", (click)="play()" disabled)
  // none      - button(type="submit" @click="play()" :style="style" disabled)
  pugAttributeSeparator: "always",

  // 结尾括号的位置
  // last-line 行末
  // new-line  新建一行
  pugClosingBracketPosition: "last-line",

  // 去掉多余空格 默认：keep-all
  // keep-all     ___this _is __a __comment_
  // keep-leading ___this is a comment
  // trim-all     this is a comment
  pugCommentPreserveSpaces: "keep-all",

  // 自定义排序规则
  pugSortAttributesBeginning: require("./pugBeautySortAttributesBeginning.js"),
  pugSortAttributesEnd: require("./pugBeautySortAttributesEnd.js"),

  // 属性排序关系
  // 'as-is' -> Foo(a c d b)
  // 'asc' -> Foo(a b c d)
  // 'desc' -> Foo(d c b a)
  pugSortAttributes: "as-is",

  // 空属性的格式
  // 'as-is' -> foo(a, b="", c)
  // 'none' -> foo(a, b, c)
  // 'all' -> foo(a="", b="", c="")
  pugEmptyAttributes: "all",

  // 属性是否换行
  // -1 自动
  // 0 始终换行
  // 1 大于1个属性才换行
  // 2 大于2个属性换行
  pugWrapAttributesThreshold: 3,

  // 匹配正则，某些属性始终换行
  // pugWrapAttributesPattern: [],
  //
  // 匹配正则，某些空属性的排序
  // pugEmptyAttributesForceQuotes: [],

  // 定义当前 pug 所在的框架， 类似 vue svelte angular 等
  pugFramework: "vue",

  // 在vue或者svelte等组件文件中，是否额外添加缩进
  pugSingleFileComponentIndentation: false,

  // 类名格式
  // 'literal'   -> foo.bar.baz
  // 'as-is'     -> foo.bar(class="baz")
  // 'attribute' -> foo(class="bar baz")
  pugClassNotation: "attribute",

  // id格式
  // 'literal' -> foo#bar
  // 'as-is' -> foo(id="bar")
  pugIdNotation: "literal",

  pugExplicitDiv: true
};
