package com.test.entity;

import com.alibaba.fastjson.JSON;
import java.util.Date;
import java.util.List;
import com.test.entity.Topic;
import com.test.entity.Reply;

@SuppressWarnings("unchecked")
public abstract class BaseUser<T> {

	/**
	 * 主键
	 * 
	 */
	private Integer id;
	/**
	 * 用户名
	 * 
	 */
	private String name;
	/**
	 * 密码
	 * 
	 */
	private String password;
	/**
	 * 性别
	 * 
	 */
	private Integer sex;
	/**
	 * 创建时间
	 * 
	 */
	private Date createTime;
	/**
	 * 删除标记
	 * 
	 */
	private Integer deleteFlag;
	/**
	 * 更新时间
	 * 
	 */
	private Date updateTime;
	/**
	 * 回复内容
	 * 
	 */
	private List<Reply> listReply;
	/**
	 * 帖子
	 * 
	 */
	private List<Topic> listTopic;

	/**
	 * 获取主键
	 * 
	 * @return 主键
	 */
	public Integer getId() {
		return id;
	}

	/**
	 * 获取用户名
	 * 
	 * @return 用户名
	 */
	public String getName() {
		return name;
	}

	/**
	 * 获取密码
	 * 
	 * @return 密码
	 */
	public String getPassword() {
		return password;
	}

	/**
	 * 获取性别
	 * 
	 * @return 性别
	 */
	public Integer getSex() {
		return sex;
	}

	/**
	 * 获取创建时间
	 * 
	 * @return 创建时间
	 */
	public Date getCreateTime() {
		return createTime;
	}

	/**
	 * 获取删除标记
	 * 
	 * @return 删除标记
	 */
	public Integer getDeleteFlag() {
		return deleteFlag;
	}

	/**
	 * 获取更新时间
	 * 
	 * @return 更新时间
	 */
	public Date getUpdateTime() {
		return updateTime;
	}

	/**
	 * 获取回复内容
	 * 
	 * @return 回复内容
	 */
	public List<Reply> getListReply() {
		return listReply;
	}

	/**
	 * 获取帖子
	 * 
	 * @return 帖子
	 */
	public List<Topic> getListTopic() {
		return listTopic;
	}

	/**
	 * 设置主键
	 * 
	 * @param id 主键对象
	 */
	public void setId(Integer id) {
		this.id = id;
	}

	/**
	 * 设置用户名
	 * 
	 * @param name 用户名对象
	 */
	public void setName(String name) {
		this.name = name;
	}

	/**
	 * 设置密码
	 * 
	 * @param password 密码对象
	 */
	public void setPassword(String password) {
		this.password = password;
	}

	/**
	 * 设置性别
	 * 
	 * @param sex 性别对象
	 */
	public void setSex(Integer sex) {
		this.sex = sex;
	}

	/**
	 * 设置创建时间
	 * 
	 * @param createTime 创建时间对象
	 */
	public void setCreateTime(Date createTime) {
		this.createTime = createTime;
	}

	/**
	 * 设置删除标记
	 * 
	 * @param deleteFlag 删除标记对象
	 */
	public void setDeleteFlag(Integer deleteFlag) {
		this.deleteFlag = deleteFlag;
	}

	/**
	 * 设置更新时间
	 * 
	 * @param updateTime 更新时间对象
	 */
	public void setUpdateTime(Date updateTime) {
		this.updateTime = updateTime;
	}

	/**
	 * 设置回复内容
	 * 
	 * @param listReply 回复内容对象
	 */
	public void setListReply(List<Reply> listReply) {
		this.listReply = listReply;
	}

	/**
	 * 设置帖子
	 * 
	 * @param listTopic 帖子对象
	 */
	public void setListTopic(List<Topic> listTopic) {
		this.listTopic = listTopic;
	}


	/**
	 * 链式添加主键
	 * 
	 * @param id 主键对象
	 * @return 对象本身
	 */
	public T chainId(Integer id) {
		this.id = id;
		return (T) this;
	}

	/**
	 * 链式添加用户名
	 * 
	 * @param name 用户名对象
	 * @return 对象本身
	 */
	public T chainName(String name) {
		this.name = name;
		return (T) this;
	}

	/**
	 * 链式添加密码
	 * 
	 * @param password 密码对象
	 * @return 对象本身
	 */
	public T chainPassword(String password) {
		this.password = password;
		return (T) this;
	}

	/**
	 * 链式添加性别
	 * 
	 * @param sex 性别对象
	 * @return 对象本身
	 */
	public T chainSex(Integer sex) {
		this.sex = sex;
		return (T) this;
	}

	/**
	 * 链式添加创建时间
	 * 
	 * @param createTime 创建时间对象
	 * @return 对象本身
	 */
	public T chainCreateTime(Date createTime) {
		this.createTime = createTime;
		return (T) this;
	}

	/**
	 * 链式添加删除标记
	 * 
	 * @param deleteFlag 删除标记对象
	 * @return 对象本身
	 */
	public T chainDeleteFlag(Integer deleteFlag) {
		this.deleteFlag = deleteFlag;
		return (T) this;
	}

	/**
	 * 链式添加更新时间
	 * 
	 * @param updateTime 更新时间对象
	 * @return 对象本身
	 */
	public T chainUpdateTime(Date updateTime) {
		this.updateTime = updateTime;
		return (T) this;
	}

	/**
	 * 链式添加回复内容
	 * 
	 * @param listReply 回复内容对象
	 * @return 对象本身
	 */
	public T chainListReply(List<Reply> listReply) {
		this.listReply = listReply;
		return (T) this;
	}

	/**
	 * 链式添加帖子
	 * 
	 * @param listTopic 帖子对象
	 * @return 对象本身
	 */
	public T chainListTopic(List<Topic> listTopic) {
		this.listTopic = listTopic;
		return (T) this;
	}


	@Override
	public String toString() {
		return JSON.toJSONString(this);
	}

}