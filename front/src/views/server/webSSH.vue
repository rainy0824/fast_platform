<template>
  <div class="app-container">
    <div id="xterm" class="xterm" />
  </div>
</template>
<script>
//引入xterm插件
import 'xterm/css/xterm.css'
import { Terminal } from 'xterm'
import { FitAddon } from 'xterm-addon-fit'
import { AttachAddon } from 'xterm-addon-attach'
import { get_server_info } from '@/api/server'
export default {
  name: 'Xterm',
  props: {
    socketURI: {
      type: String,
      default: `${process.env.VUE_APP_WS_API}/servers/web_terminal`
    }
  },
  data() {
    return {
      serverinfo: null
    }
  },
  mounted() {
    this.initSocket()

  },
  beforeDestroy() {
    this.socket.close()
    this.term.dispose()
  },
  methods: {
    async getServerInfo() {
      // 通过id去获取服务器信息
      await get_server_info(this.$route.params.server_id).then(response => {
        this.serverinfo = response

      })
    },
    initTerm() {
      // 计算高度和宽度
      
      const initWidth = 9
      const initHeight = 17
      const cols = Math.floor(window.innerWidth / initWidth)
      const rows = Math.floor(window.innerHeight / initHeight) - 3
      const term = new Terminal({
        rendererType: 'canvas', // 渲染类型
        convertEol: true, // 启用时，光标将设置为下一行的开头
        disableStdin: false, // 是否应禁用输入。
        cursorBlink: true, // 光标闪烁
        cols: cols,
        rows: rows,
        theme: {
          foreground: 'yellow', // 字体
          background: '#111111', // 背景色
          cursor: 'help' // 设置光标
        }
      })
      const attachAddon = new AttachAddon(this.socket)
      const fitAddon = new FitAddon()
      term.loadAddon(attachAddon)
      term.loadAddon(fitAddon)
      term.open(document.getElementById('xterm'))
      fitAddon.fit()
      term.focus()
      this.term = term
    },
    async initSocket() {

      await this.getServerInfo()
      let params=`?server_ip=${this.serverinfo.server_ip}&server_port=${this.serverinfo.server_port}&server_login_name=${this.serverinfo.server_login_name}&server_login_pwd=${this.serverinfo.server_login_pwd}`
      this.socket = new WebSocket(this.socketURI+params)
      this.socketOnClose()
      this.socketOnOpen()
      this.socketOnError()
    },
    socketOnOpen() {
      this.socket.onopen = () => {
        // 链接成功后
        this.initTerm()
      }
    },
    socketOnClose() {
      this.socket.onclose = () => {
        this.$alert('连接已经断开', 'Tips', {
          confirmButtonText: '退出',
          callback: action => {
            window.close()
          }
        })
      }
    },
    socketOnError() {
      this.socket.onerror = () => {
        this.$alert('连接失败,请联系管理员', 'Tips', {
          confirmButtonText: '退出',
          callback: action => {
            window.close()
          }
        })
      }
    }
  }
}
</script>
