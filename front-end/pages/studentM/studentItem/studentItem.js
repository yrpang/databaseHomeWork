// pages/departmentM/departmentItem/departmentItem.js
const app = getApp()
Page({
  data: {
    ifnew: false,
    classIndex: -1
  },

  onLoad: function (options) {
    this.data.id = options.id
    if (options.id == -1) {
      wx.request({
        url: app.globalData.baseURL + 'class',
        method: "GET",
        success: res => {
          console.log(res.data)
          this.setData({
            data: {
              classIndex: -1
            },
            ifnew: true,
            classes: res.data.data
          })
        }
      })
    } else {
      wx.request({
        url: app.globalData.baseURL + 'class',
        method: "GET",
        success: res => {
          // console.log(res.data.data)
          wx.request({
            url: app.globalData.baseURL + 'student/' + options.id,
            method: "GET",
            success: res2 => {
              console.log(res2.data)
              console.log("上面是学生信息")
              var index = res.data.data.findIndex((item) =>
                item.classNo == res2.data.data.classNo
              )
              this.setData({
                classes: res.data.data,
                data: res2.data.data,
                classIndex: index
              })
            }
          })
        }
      })
    }
  },

  noInput: function (e) {
    this.setData({
      ["data.stuNo"]: e.detail.value
    })
  },

  nameInput: function (e) {
    this.setData({
      ["data.stuName"]: e.detail.value
    })
  },

  ageInput: function (e) {
    this.setData({
      ["data.stuAge"]: e.detail.value
    })
  },

  bindChange: function (e) {
    console.log(e)
    this.setData({
      classIndex: e.detail.value,
      ["data.classNo"]: this.data.classes[e.detail.value]['classNo']
    })
  },

  submit: function () {
    if (!this.data.data.stuName || !this.data.data.stuAge || !this.data.data.stuNo) {
      this.setData({
        error: "所有字段不能为空"
      })
      return
    }
    // console.log(this.data.id)
    wx.request({
      url: app.globalData.baseURL + 'student/' + this.data.id,
      method: "PUT",
      data: {
        stuName: this.data.data.stuName,
        stuAge: this.data.data.stuAge,
        classNo: this.data.data.classNo
      },
      success: res => {
        console.log(res)
        if(res.data.statusCode != 200)
        {
          wx.showModal({
            title: "错误",
            content: "请检查字段格式",
            showCancel: false,
            success(res) {
            }
          })
        }
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
            showCancel: false,
            success(res) {
            }
          })
        }
      }
    })
  },

  create: function () {
    if (!this.data.data.stuNo || !this.data.data.stuName || !this.data.data.stuAge || !this.data.data.classNo) {
      this.setData({
        error: "所有字段不能为空"
      })
      return
    }
    wx.request({
      url: app.globalData.baseURL + 'student',
      method: "POST",
      data: {
        stuNo: this.data.data.stuNo,
        stuName: this.data.data.stuName,
        stuAge: this.data.data.stuAge,
        classNo: String(this.data.data.classNo)
      },
      success: res => {
        console.log(res)
        if(res.data.statusCode != 200)
        {
          wx.showModal({
            title: "错误",
            content: "请检查字段格式",
            showCancel: false,
            success(res) {
            }
          })
        }
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
            showCancel: false,
            success(res) {
            }
          })
        }
      }
    })
  },

  toSociety: function (e) {
    console.log(e)
    var info = {
      id: e.currentTarget.id,
      checked: this.data.data.society
    }
    wx.navigateTo({
      url: '../society/society?info=' + JSON.stringify(info),
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