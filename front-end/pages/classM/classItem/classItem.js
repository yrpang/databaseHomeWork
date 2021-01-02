// pages/departmentM/departmentItem/departmentItem.js
const app = getApp()
Page({
  data: {
    ifnew: false,
    departsIndex: -1
  },

  onLoad: function (options) {
    this.data.id = options.id
    if (options.id == -1) {
      wx.request({
        url: app.globalData.baseURL + 'department',
        method: "GET",
        success: res => {
          console.log(res.data)
          this.setData({
            data: {
              classNo: "",
              className: "",
              classYear: "",
              departNo: -1
            },
            ifnew: true,
            departs: res.data.data
          })
        }
      })
    } else {
      wx.request({
        url: app.globalData.baseURL + 'class/' + options.id,
        method: "GET",
        success: res => {
          // console.log(res.data),
          this.setData({
            data: res.data.data
          })
          wx.request({
            url: app.globalData.baseURL + 'department',
            method: "GET",
            success: res2 => {
              console.error(res2.data)
              console.log(res.data.data.departName)
              var index = res2.data.data.findIndex((item) =>
                item.departName == res.data.data.departName
              )
              this.setData({
                departs: res2.data.data,
                departsIndex: index
              })
            }
          })
        }
      })

    }
  },

  nameInput: function (e) {
    this.setData({
      ["data.className"]: e.detail.value
    })
  },

  noInput: function (e) {
    this.setData({
      ["data.classNo"]: e.detail.value
    })
  },

  yearInput: function (e) {
    this.setData({
      ["data.classYear"]: e.detail.value
    })
  },

  bindChange: function (e) {
    console.log(e)
    this.setData({
      departsIndex: e.detail.value
    })
  },

  // 添加departInput

  submit: function () {
    if (!this.data.data.className || !this.data.data.classNo || !this.data.data.classYear) {
      this.setData({
        error: "所有字段不能为空"
      })
      return
    }
    console.log(this.data.id)
    wx.request({
      url: app.globalData.baseURL + 'class/' + this.data.id,
      method: "PUT",
      data: {
        className: this.data.data.className,
        classYear: this.data.data.classYear,
        departNo: this.data.departs[this.data.departsIndex].departNo
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
    if (!this.data.data.className || !this.data.data.classNo || !this.data.data.classYear) {
      this.setData({
        error: "所有字段不能为空"
      })
      return
    }
    wx.request({
      url: app.globalData.baseURL + 'class',
      method: "POST",
      data: {
        classNo: this.data.data.classNo,
        className: this.data.data.className,
        classYear: this.data.data.classYear,
        departNo: this.data.departs[this.data.departsIndex].departNo
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