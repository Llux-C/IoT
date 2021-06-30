<template>
  <div class="help" style="minHeight:calc(100vh - 139px)">
    <a-card hoverable style="width: 100%" :bordered="false">
      <a-card-meta title="操作问题详见用户手册" description="遇到解决不了的问题请点击“联系我们”">
      </a-card-meta>
    </a-card>
    <a-card hoverable style="width: 100%" :bordered="false">
      <a-card-meta title="运行问题详见运行开发指南手册" description="遇到解决不了的问题请点击“联系我们”">
      </a-card-meta>
    </a-card>
    <a-card hoverable style="width: 100%" :bordered="false">
      <a-card-meta title="欢迎提出PR，详见接口文档手册" description="遇到解决不了的问题请点击“联系我们”">
      </a-card-meta>
    </a-card>
  </div>
</template>

<script>

export default {
  name: 'Help',
  components: {
  }
}
</script>
