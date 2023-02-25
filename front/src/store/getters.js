/*
 * @Author: error: git config user.name && git config user.email & please set dead value or install git
 * @Date: 2022-09-23 14:40:55
 * @LastEditors: error: git config user.name && git config user.email & please set dead value or install git
 * @LastEditTime: 2022-12-10 00:23:52
 * @FilePath: /front/src/store/getters.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
const getters = {
  sidebar: state => state.app.sidebar,
  device: state => state.app.device,
  visitedViews: state => state.tagsView.visitedViews, //访问过的视图
  cachedViews: state => state.tagsView.cachedViews, //缓存视图
  token: state => state.user.token,
  avatar: state => state.user.avatar,
  // 昵称
  name: state => state.user.name,
  // 菜单
  menus: state => state.user.menus,
  // 权限路由
  permission_routes: state => state.permission.routes
}
export default getters
