package com.test.mapper;

import java.util.List;
import chiya.core.base.page.Page;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import com.test.entity.Reply;
;
import com.test.entity.Topic;
;

@Mapper
public interface BaseUserMapper {

	/**
	 * 添加用户表
	 * 
	 * @param user 用户表
	 * @return 受影响行数
	 */
	Integer insertUser(User user);

	/**
	 * 添加多个用户表
	 * 
	 * @param list 用户表列表
	 * @return 受影响行数
	 */
	Integer insertUserList(@Param("list") List<User> list);

	/**
	 * 添加或更新用户表，根据唯一性索引
	 * 
	 * @param list 用户表列表
	 * @return 受影响行数
	 */
	Integer insertOrUpdateUserByUnique(User user);

	/**
	 * 添加或更新用户表，根据查询条件
	 * 
	 * @param saveUser 添加的用户表对象
	 * @param conditionUser 用户表条件对象
	 * @return 受影响行数
	 */
	Integer insertOrUpdateUserByWhere(@Param("saveUser") User saveUser, @Param("conditionUser") User conditionUser);

	/**
	 * 条件添加用户表
	 * 
	 * @param saveUser 添加的用户表对象
	 * @param conditionUser 用户表条件对象
	 * @return 受影响行数
	 */
	Integer insertUserByWhereOnlySave(@Param("saveUser") User saveUser, @Param("conditionUser") User conditionUser);

	/**
	 * 根据id真删用户表
	 * 
	 * @param id 用户表的id
	 * @return 受影响行数
	 */
	Integer deleteUserById(Integer id);

	/**
	 * 根据id列表真删用户表
	 * 
	 * @param list 用户表的id列表
	 * @return 受影响行数
	 */
	Integer deleteUserInId(List<Integer> list);

	/**
	 * 根据id和其他条件真删用户表
	 * 
	 * @param id 用户表的id
	 * @param user 用户表条件对象
	 * @return 受影响行数
	 */
	Integer deleteUserByIdAndWhere(@Param("id") Integer id, @Param("user") User user);

	/**
	 * 根据条件真删用户表
	 * 
	 * @param user 用户表条件对象
	 * @return 受影响行数
	 */
	Integer deleteUser(User user);

	/**
	 * 根据id假删用户表
	 * 
	 * @param id 用户表的id
	 * @return 受影响行数
	 */
	Integer falseDeleteUserById(Integer id);

	/**
	 * 根据id修改用户表
	 * 
	 * @param user 要更新的用户表对象
	 * @return 受影响行数
	 */
	Integer updateUserById(User user);

	/**
	 * 根据id和不满足的条件更新用户表，查询条件不满足时更新对象
	 * 
	 * @param saveUser 更新的用户表对象
	 * @param conditionUser 不存在的用户表对象
	 * @return 受影响行数
	 */
	Integer updateUserByNotRepeatWhere(@Param("saveUser") User saveUser, @Param("conditionUser") User conditionUser);

	/**
	 * 根据id和其他的条件更新用户表
	 * 
	 * @param saveUser 更新的用户表对象
	 * @param conditionUser 用户表条件对象
	 * @return 受影响行数
	 */
	Integer updateUserByIdAndWhere(@Param("saveUser") User saveUser, @Param("conditionUser") User conditionUser);

	/**
	 * 根据条件更新用户表
	 * 
	 * @param saveUser 更新的用户表对象
	 * @param conditionUser 条件用户表对象
	 * @return 受影响行数
	 */
	Integer updateUser(@Param("saveUser") User saveUser, @Param("conditionUser") User conditionUser);

	/**
	 * 记录id设置其他字段为null
	 * 
	 * @param user 设置成null的用户表对象，对象中字段不为Null则是要设置成null的字段
	 * @return 受影响行数
	 */
	Integer updateUserSetNullById(User user);

	/**
	 * 根据id查询用户表
	 * 
	 * @param id 用户表的id
	 * @return 用户表对象
	 */
	User selectUserById(Integer id);

	/**
	 * 根据id列表查询用户表
	 * 
	 * @param list 用户表的id列表
	 * @return 用户表对象列表
	 */
	List<User> selectUserInId(List<Integer> list);

	/**
	 * 只查询一个用户表
	 * 
	 * @param user 用户表对象
	 * @param index 获取的下标值
	 * @return 用户表对象
	 */
	User selectOneUser(@Param("user")User user, @Param("index")Integer index);

	/**
	 * 查询多个用户表
	 * 
	 * @param user 用户表对象
	 * @param page 分页对象
	 * @return 用户表对象列表
	 */
	List<User> selectUser(@Param("user")User user, @Param("page") Page page);

	/**
	 * 统计用户表记录数
	 * 
	 * @param user 用户表对象
	 * @return 查询到的记录数
	 */
	Integer countUser(@Param("user")User user);

	/**
	 * 内联一对多查询回复内容，双方均可分页
	 * 
	 * @param user 用户表对象
	 * @param reply 回复内容对象
	 * @param onePage 用户表分页对象
	 * @param manyPage 回复内容分页对象
	 * @return 用户表对象列表
	 */
	List<User> findUserOneToManyReply(@Param("user") User user, @Param("reply") Reply reply, @Param("onePage") Page onePage, @Param("manyPage") Page manyPage);

	/**
	 * 内联一对多统计回复内容，双方均可分页
	 * 
	 * @param user 用户表对象
	 * @param reply 回复内容对象
	 * @param onePage 用户表分页对象
	 * @param manyPage 回复内容分页对象
	 * @return 查询到的记录数
	 */
	Integer countFindUserOneToManyReply(@Param("user") User user, @Param("reply") Reply reply, @Param("onePage") Page onePage, @Param("manyPage") Page manyPage);

	/**
	 * 内联一对多查询回复内容，只返回回复内容
	 * 
	 * @param user 用户表对象
	 * @param reply 回复内容对象
	 * @param onePage 用户表分页对象
	 * @param manyPage 回复内容分页对象
	 * @return 用户表对象列表
	 */
	List<Reply> linkOneToManyReply(@Param("user") User user, @Param("reply") Reply reply, @Param("onePage") Page onePage, @Param("manyPage") Page manyPage);

	/**
	 * 外联一对多查询回复内容，双方均可分页
	 * 
	 * @param user 用户表对象
	 * @param reply 回复内容对象
	 * @param onePage 用户表分页对象
	 * @param manyPage 回复内容分页对象
	 * @return 用户表对象列表
	 */
	List<User> queryUserOneToManyReply(@Param("user") User user, @Param("reply") Reply reply, @Param("onePage") Page onePage, @Param("manyPage") Page manyPage);

	/**
	 * 内联一对多查询帖子，双方均可分页
	 * 
	 * @param user 用户表对象
	 * @param topic 帖子对象
	 * @param onePage 用户表分页对象
	 * @param manyPage 帖子分页对象
	 * @return 用户表对象列表
	 */
	List<User> findUserOneToManyTopic(@Param("user") User user, @Param("topic") Topic topic, @Param("onePage") Page onePage, @Param("manyPage") Page manyPage);

	/**
	 * 内联一对多统计帖子，双方均可分页
	 * 
	 * @param user 用户表对象
	 * @param topic 帖子对象
	 * @param onePage 用户表分页对象
	 * @param manyPage 帖子分页对象
	 * @return 查询到的记录数
	 */
	Integer countFindUserOneToManyTopic(@Param("user") User user, @Param("topic") Topic topic, @Param("onePage") Page onePage, @Param("manyPage") Page manyPage);

	/**
	 * 内联一对多查询帖子，只返回帖子
	 * 
	 * @param user 用户表对象
	 * @param topic 帖子对象
	 * @param onePage 用户表分页对象
	 * @param manyPage 帖子分页对象
	 * @return 用户表对象列表
	 */
	List<Topic> linkOneToManyTopic(@Param("user") User user, @Param("topic") Topic topic, @Param("onePage") Page onePage, @Param("manyPage") Page manyPage);

	/**
	 * 外联一对多查询帖子，双方均可分页
	 * 
	 * @param user 用户表对象
	 * @param topic 帖子对象
	 * @param onePage 用户表分页对象
	 * @param manyPage 帖子分页对象
	 * @return 用户表对象列表
	 */
	List<User> queryUserOneToManyTopic(@Param("user") User user, @Param("topic") Topic topic, @Param("onePage") Page onePage, @Param("manyPage") Page manyPage);

}