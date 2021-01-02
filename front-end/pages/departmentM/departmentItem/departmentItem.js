// pages/departmentM/departmentItem/departmentItem.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    ifnew: false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.data.id = options.id
    if (options.id == -1) {
      this.setData({
        data: {
          departNum: "",
          departOffice: "",
          dormitoryNo: "",
          departNum: 0
        },
        ifnew: true
      })
      return
    }
    wx.request({
      url: app.globalData.baseURL + 'department/' + options.id,
      method: "GET",
      success: res => {
        console.log(res.data),
          this.setData({
            data: res.data.data
          })
      }
    })
  },

  nameInput: function (e) {
    this.setData({
      ["data.departName"]: e.detail.value
    })
  },

  locInput: function (e) {
    this.setData({
      ["data.dormitoryNo"]: e.detail.value
    })
  },

  officeInput: function (e) {
    this.setData({
      ["data.departOffice"]: e.detail.value
    })
  },

  submit: function () {
    if (!this.data.data.departName || !this.data.data.departOffice || !this.data.data.dormitoryNo) {
      this.setData({
        error: "所有字段不能为空"
      })
      return
    }
    wx.request({
      url: app.globalData.baseURL + 'department/' + this.data.id,
      method: "PUT",
      data: {
        departName: this.data.data.departName,
        departOffice: this.data.data.departOffice,
        dormitoryNo: this.data.data.dormitoryNo
      },
      success: res => {
        console.log(res)
        if (res.data.errCode == 0) {
          wx.showModal({
            title: "成功",
            content: "修改完成",
            showCancel: false,
            success(res) {
              if (res.confirm) {
                wx.navigateBack()
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
  },

  create: function () {
    if (!this.data.data.departName || !this.data.data.departOffice || !this.data.data.dormitoryNo) {
      this.setData({
        error: "所有字段不能为空"
      })
      return
    }
    wx.request({
      url: app.globalData.baseURL + 'department',
      method: "POST",
      data: {
        departName: this.data.data.departName,
        departOffice: this.data.data.departOffice,
        dormitoryNo: this.data.data.dormitoryNo
      },
      success: res => {
        console.log(res)
        if (res.data.errCode == 0) {
          wx.showModal({
            title: "成功",
            content: "添加完成",
            showCancel: false,
            success(res) {
              if (res.confirm) {
                wx.navigateBack()
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
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})