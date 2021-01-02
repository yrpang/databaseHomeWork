//index.js
//获取应用实例
const app = getApp()

Page({
  data: {

  },

  toClassM: function () {
    wx.navigateTo({
      url: '../classM/classAll/classAll',
    })
  },

  tosocietyM: function () {
    wx.navigateTo({
      url: '../societyM/society/society',
    })
  },

  toDepartmentM: function () {
    wx.navigateTo({
      url: '../departmentM/department/department',
    })
  },

  tostudentM: function () {
    wx.navigateTo({
      url: '../studentM/studentAll/studentAll',
    })
  },

  toClassChange: function () {
    wx.navigateTo({
      url: '../changeClassNo/changeClassNo',
    })
  },

  fixNum: function () {
    wx.request({
      url: app.globalData.baseURL + 'manage/fixNum',
      method: 'GET',
      success: res=>{
        if (res.data.errCode == 0) {
          wx.showModal({
            title: "成功",
            content: res.data.data,
            showCancel: false,
            success(res) {
              if (res.confirm) {
              }
            }
          })
        } else {
          wx.showModal({
            title: "错误",
            content: res.data.status,
            showCancel: false
          })
        }
      }
    })
  }
})